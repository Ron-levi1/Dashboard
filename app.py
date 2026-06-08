
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO


# ============================================================
# הגדרות עמוד
# ============================================================

st.set_page_config(
    page_title="דשבורד מחקרים קליניים",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# עיצוב RTL
# ============================================================

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: Arial, sans-serif;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3, h4 {
        text-align: right;
    }

    div[data-testid="stMetric"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 16px;
        border-radius: 16px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }

    div[data-testid="stMetricValue"] {
        font-size: 23px;
        font-weight: 700;
    }

    .info-box {
        background-color: #f1f5f9;
        border-right: 5px solid #0ea5e9;
        padding: 14px 18px;
        border-radius: 12px;
        margin-bottom: 16px;
    }

    .warn-box {
        background-color: #fff7ed;
        border-right: 5px solid #f97316;
        padding: 14px 18px;
        border-radius: 12px;
        margin-bottom: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# פונקציות עזר
# ============================================================

def normalize_text(value):
    if pd.isna(value):
        return ""
    value = str(value)
    value = value.replace("\u200f", "").replace("\u200e", "")
    value = value.replace("–", "-").replace("—", "-").replace("−", "-")
    value = value.replace("״", '"').replace("”", '"').replace("“", '"')
    value = " ".join(value.split())
    return value.strip()


def normalize_columns(df):
    df = df.copy()
    df.columns = [normalize_text(col) for col in df.columns]
    return df


def find_col(df, candidates):
    normalized = {normalize_text(col): col for col in df.columns}
    for c in candidates:
        c_norm = normalize_text(c)
        if c_norm in normalized:
            return normalized[c_norm]
    return None


def to_numeric(series):
    return (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("₪", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace("€", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip()
        .replace({"": np.nan, "nan": np.nan, "None": np.nan})
        .pipe(pd.to_numeric, errors="coerce")
        .fillna(0)
    )


def make_numeric(df, cols):
    df = df.copy()
    for col in cols:
        if col and col in df.columns:
            df[col] = to_numeric(df[col])
    return df


def to_date(series):
    return pd.to_datetime(series, errors="coerce", dayfirst=True)


def money(value):
    try:
        return f"{float(value):,.0f} ₪"
    except Exception:
        return "0 ₪"


def number(value):
    try:
        return f"{float(value):,.0f}"
    except Exception:
        return "0"


def pct(value):
    try:
        return f"{float(value):,.1f}%"
    except Exception:
        return "0%"


def sum_col(df, col):
    if col and col in df.columns:
        return to_numeric(df[col]).sum()
    return 0


def count_unique_studies(df, unique_col, study_id_col):
    if unique_col and unique_col in df.columns:
        s = to_numeric(df[unique_col]).sum()
        if s > 0:
            return s
    if study_id_col and study_id_col in df.columns:
        return df[study_id_col].dropna().astype(str).nunique()
    return len(df)


def download_excel(sheets_dict):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for sheet_name, df in sheets_dict.items():
            safe_name = str(sheet_name)[:31]
            df.to_excel(writer, index=False, sheet_name=safe_name)
    return output.getvalue()


def budget_status(value):
    try:
        value = float(value)
    except Exception:
        return "לא ידוע"

    if value < 20:
        return "ניצול נמוך"
    elif value <= 80:
        return "תקין"
    elif value <= 100:
        return "קרוב לניצול מלא"
    else:
        return "חריגה"


def traffic_light(status, balance=None, days_to_end=None, recruitment_pct=None):
    if status == "חריגה":
        return "🔴 אדום"

    if balance is not None:
        try:
            if float(balance) < 0:
                return "🔴 אדום"
        except Exception:
            pass

    if days_to_end is not None:
        try:
            if 0 <= float(days_to_end) <= 60:
                return "🟡 צהוב"
        except Exception:
            pass

    if recruitment_pct is not None:
        try:
            if float(recruitment_pct) < 50:
                return "🟡 צהוב"
        except Exception:
            pass

    if status in ["ניצול נמוך", "קרוב לניצול מלא", "לא ידוע"]:
        return "🟡 צהוב"

    return "🟢 ירוק"


def plot_bar(df, x, y, title, horizontal=False):
    if df.empty or x not in df.columns or y not in df.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    if horizontal:
        fig = px.bar(df, x=y, y=x, orientation="h", text=y, title=title)
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
    else:
        fig = px.bar(df, x=x, y=y, text=y, title=title)

    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig.update_layout(title_x=0.5, height=500, margin=dict(l=20, r=20, t=80, b=80))
    st.plotly_chart(fig, use_container_width=True)


def plot_grouped_bar(df, x, y_cols, title):
    y_cols = [c for c in y_cols if c and c in df.columns]
    if df.empty or x not in df.columns or not y_cols:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    fig = px.bar(df, x=x, y=y_cols, barmode="group", title=title)
    fig.update_layout(title_x=0.5, height=500, margin=dict(l=20, r=20, t=80, b=80))
    st.plotly_chart(fig, use_container_width=True)


def plot_pie(df, names, values, title):
    if df.empty or names not in df.columns or values not in df.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    fig = px.pie(df, names=names, values=values, hole=0.35, title=title)
    fig.update_layout(title_x=0.5, height=500)
    st.plotly_chart(fig, use_container_width=True)


def top10_other(df, group_col, value_col, value_name):
    if not group_col or not value_col or group_col not in df.columns or value_col not in df.columns:
        return pd.DataFrame()

    temp = df.copy()
    temp[value_col] = to_numeric(temp[value_col])

    grouped = (
        temp.groupby(group_col, as_index=False)[value_col]
        .sum()
        .sort_values(value_col, ascending=False)
        .rename(columns={group_col: "שם", value_col: value_name})
    )

    top10 = grouped.head(10)
    other_sum = grouped.iloc[10:][value_name].sum()

    if other_sum > 0:
        top10 = pd.concat(
            [top10, pd.DataFrame({"שם": ["אחר"], value_name: [other_sum]})],
            ignore_index=True
        )

    return top10


def sidebar_filter(df, label, col):
    if not col or col not in df.columns:
        return df

    values = sorted(df[col].dropna().astype(str).unique())
    selected = st.sidebar.multiselect(label, values)

    if selected:
        return df[df[col].astype(str).isin(selected)]

    return df


# ============================================================
# כותרת והעלאת קובץ
# ============================================================

st.title("📊 דשבורד ניהולי למחקרים קליניים")

st.markdown(
    """
    <div class="info-box">
    העלי קובץ Excel הכולל את גיליון <b>studies_data</b> וגיליון פירוט הוצאות והכנסות פר מחקר.
    הדשבורד יציג ניתוח ברמת כלל בית החולים, מחלקות, חוקרים, יזמים, סטטוס תקציבי ודוחות לחוקר.
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("העלי קובץ Excel", type=["xlsx"])

if uploaded_file is None:
    st.info("יש להעלות קובץ Excel כדי להתחיל.")
    st.stop()

try:
    xls = pd.ExcelFile(uploaded_file)
except Exception as e:
    st.error("לא הצלחתי לקרוא את קובץ האקסל.")
    st.write(e)
    st.stop()

sheet_names = xls.sheet_names
st.success("הקובץ נטען בהצלחה.")

default_studies_index = 0
for i, s in enumerate(sheet_names):
    if normalize_text(s).lower() == "studies_data":
        default_studies_index = i

studies_sheet = st.selectbox(
    "בחרי את גיליון studies_data",
    sheet_names,
    index=default_studies_index
)

details_sheet = st.selectbox(
    "בחרי את גיליון פירוט הוצאות והכנסות פר מחקר",
    sheet_names,
    index=1 if len(sheet_names) > 1 else 0
)

studies_df = normalize_columns(pd.read_excel(uploaded_file, sheet_name=studies_sheet))
details_df = normalize_columns(pd.read_excel(uploaded_file, sheet_name=details_sheet))


# ============================================================
# מיפוי עמודות studies_data
# ============================================================

C = {
    "approval_date": find_col(studies_df, ["תאריך אישור מחקר"]),
    "approval_year": find_col(studies_df, ["שנת אישור המחקר", "שנת אישור מחקר"]),
    "start_date": find_col(studies_df, ["תאריך תחילה"]),
    "end_date": find_col(studies_df, ["תאריך סיום"]),
    "protocol": find_col(studies_df, ["סימון פרוטוקול", "מספר פרוטוקול"]),
    "study_id": find_col(studies_df, ["סוג תכנית-study_id", "סוג תכנית – study_id", "סוג תכנית - study_id", "מספר הלסינקי"]),
    "pi": find_col(studies_df, ["חוקר ראשי", "שם חוקר ראשי"]),
    "site": find_col(studies_df, ["site", "SITE"]),
    "department": find_col(studies_df, ["מחלקה"]),
    "sub_department": find_col(studies_df, ["תת-מחלקה"]),
    "study_type": find_col(studies_df, ["סוג המחקר"]),
    "phase": find_col(studies_df, ["פאזת המחקר", "פאזה"]),
    "coordinator": find_col(studies_df, ["מתאמת ראשית"]),
    "sponsor": find_col(studies_df, ["יזם", "גורם מממן"]),
    "funding_type": find_col(studies_df, ["סוג מימון"]),
    "expected_income": find_col(studies_df, ["צפי הכנסות (₪)", "צפי הכנסות ₪"]),
    "actual_income": find_col(studies_df, ["הכנסות בפועל"]),
    "total_expenses": find_col(studies_df, ["סך ההוצאות"]),
    "salary_expenses": find_col(studies_df, ["הוצאות- שכר", "הוצאות - שכר"]),
    "materials_expenses": find_col(studies_df, ["הוצאות- מתכלים", "הוצאות - מתכלים"]),
    "fixed_expenses": find_col(studies_df, ["הוצאות- קבוע", "הוצאות - קבוע"]),
    "travel_expenses": find_col(studies_df, ["הוצאות- נסיעות", "הוצאות - נסיעות"]),
    "internal_expenses": find_col(studies_df, ["הוצאות- העברות פנימיות", "הוצאות - העברות פנימיות"]),
    "expected_participants": find_col(studies_df, ["צפי משתתפים"]),
    "actual_participants": find_col(studies_df, ["משתתפים בפועל"]),
    "unique_study": find_col(studies_df, ["unique_study"]),
    "unique_researcher": find_col(studies_df, ["unique_researcher"]),
    "contract": find_col(studies_df, ["מספר מרכבה- מספר חוזה", "מספר מרכבה - מספר חוזה", "מספר חוזה"]),
    "budget_name": find_col(studies_df, ["שם תקציב"]),
    "budget_owner": find_col(studies_df, ["עובד אחראי- שם בעל התקציב", "עובד אחראי - שם בעל התקציב", "שם בעל התקציב"]),
    "country": find_col(studies_df, ["ארץ/חו\"ל- עדיפות", "ארץ/חו\"ל - עדיפות"]),
    "wbs": find_col(studies_df, ["אלמנט WBS", "מספר WBS"]),
    "budget": find_col(studies_df, ["תקציב"]),
    "overhead": find_col(studies_df, ["תקורה לפי 18%", "תקורה"]),
    "commitment": find_col(studies_df, ["התחייבות", "התחייבויות"]),
    "execution": find_col(studies_df, ["ביצוע"]),
    "utilization_total": find_col(studies_df, ["סה\"כ ניצול (₪)", "סהכ ניצול (₪)", "סה\"כ ניצול"]),
    "utilization_pct": find_col(studies_df, ["% ניצול תקציב", "אחוז ניצול תקציב"]),
    "balance": find_col(studies_df, ["יתרה לניצול"]),
    "utilization_group": find_col(studies_df, ["קבוצות ניצול"]),
    "unreserved_balance": find_col(studies_df, ["יתרה לא משוריינת"]),
    "status": find_col(studies_df, ["סטטוס"]),
    "traffic_light": find_col(studies_df, ["רמזור"]),
    "research_class": find_col(studies_df, ["סיווג מחקר (תקן 40)- סוג פרויקט", "סיווג מחקר (תקן 40) - סוג פרויקט", "סוג פרויקט"]),
    "gl_account": find_col(studies_df, ["חשבון GL"]),
    "gl_name": find_col(studies_df, ["שם חשבון GL"]),
}


# ============================================================
# מיפוי עמודות גיליון פירוט
# ============================================================

D = {
    "wbs": find_col(details_df, ["אלמנט WBS", "מספר WBS"]),
    "fund_center": find_col(details_df, ["מרכז קרנות"]),
    "commitment_group": find_col(details_df, ["קבוצת פריט התחייבות"]),
    "commitment_group_desc": find_col(details_df, ["תיאור קבוצת פריט התחייבות"]),
    "pi_code": find_col(details_df, ["חוקר ראשי – לא שם אלא קוד", "חוקר ראשי - לא שם אלא קוד"]),
    "pi_name": find_col(details_df, ["שם חוקר ראשי", "חוקר ראשי"]),
    "protocol": find_col(details_df, ["מספר פרוטוקול"]),
    "study_id": find_col(details_df, ["מספר הלסינקי"]),
    "protocol_name": find_col(details_df, ["פרוטוקול"]),
    "site": find_col(details_df, ["site", "SITE"]),
    "budget_category": find_col(details_df, ["קטגוריית סעיף תקציבי"]),
    "commitment_item": find_col(details_df, ["פריט התחייבות"]),
    "description": find_col(details_df, ["תיאור"]),
    "budget_total": find_col(details_df, ["סה\"כ תקציב מ", "סהכ תקציב מ"]),
    "purchase_commitments": find_col(details_df, ["התחייבויות רכש"]),
    "execution_total": find_col(details_df, ["סה\"כ ביצוע", "סהכ ביצוע"]),
    "balance": find_col(details_df, ["יתרה לניצול"]),
}


# ============================================================
# ניקוי וחישובים
# ============================================================

numeric_studies_cols = [
    C["expected_income"], C["actual_income"], C["total_expenses"],
    C["salary_expenses"], C["materials_expenses"], C["fixed_expenses"],
    C["travel_expenses"], C["internal_expenses"], C["expected_participants"],
    C["actual_participants"], C["unique_study"], C["unique_researcher"],
    C["budget"], C["overhead"], C["commitment"], C["execution"],
    C["utilization_total"], C["utilization_pct"], C["balance"], C["unreserved_balance"]
]

numeric_details_cols = [
    D["budget_total"], D["purchase_commitments"], D["execution_total"], D["balance"]
]

df = make_numeric(studies_df, numeric_studies_cols)
details = make_numeric(details_df, numeric_details_cols)

for date_col in [C["approval_date"], C["start_date"], C["end_date"]]:
    if date_col and date_col in df.columns:
        df[date_col] = to_date(df[date_col])

if C["approval_year"] is None and C["approval_date"]:
    df["שנת אישור המחקר - מחושב"] = df[C["approval_date"]].dt.year
    C["approval_year"] = "שנת אישור המחקר - מחושב"

if C["utilization_pct"]:
    util = to_numeric(df[C["utilization_pct"]])
    if util.max() <= 1.5 and util.max() > 0:
        util = util * 100
    df["% ניצול תקציב - מחושב"] = util
elif C["budget"] and C["utilization_total"]:
    budget = to_numeric(df[C["budget"]])
    util_total = to_numeric(df[C["utilization_total"]])
    df["% ניצול תקציב - מחושב"] = np.where(budget > 0, util_total / budget * 100, 0)
else:
    df["% ניצול תקציב - מחושב"] = 0

df["סטטוס ניצול תקציב - מחושב"] = df["% ניצול תקציב - מחושב"].apply(budget_status)

if C["expected_participants"] and C["actual_participants"]:
    expected = to_numeric(df[C["expected_participants"]])
    actual = to_numeric(df[C["actual_participants"]])
    df["% גיוס משתתפים"] = np.where(expected > 0, actual / expected * 100, 0)
else:
    df["% גיוס משתתפים"] = 0

def recruitment_status(value):
    try:
        value = float(value)
    except Exception:
        return "לא ידוע"
    if value == 0:
        return "אין גיוס"
    elif value < 50:
        return "גיוס נמוך"
    elif value < 80:
        return "גיוס בינוני"
    else:
        return "גיוס תקין"

df["סטטוס גיוס"] = df["% גיוס משתתפים"].apply(recruitment_status)

if C["end_date"]:
    today = pd.Timestamp.today().normalize()
    df["ימים לסיום"] = (df[C["end_date"]] - today).dt.days
else:
    df["ימים לסיום"] = np.nan

df["רמזור ניהולי"] = df.apply(
    lambda row: traffic_light(
        row["סטטוס ניצול תקציב - מחושב"],
        row[C["balance"]] if C["balance"] else None,
        row["ימים לסיום"],
        row["% גיוס משתתפים"]
    ),
    axis=1
)


# ============================================================
# פילטרים כלליים
# ============================================================

st.sidebar.header("🔎 פילטרים כלליים")

filtered = df.copy()
filtered = sidebar_filter(filtered, "שנת אישור המחקר", C["approval_year"])
filtered = sidebar_filter(filtered, "מחלקה", C["department"])
filtered = sidebar_filter(filtered, "חוקר ראשי", C["pi"])
filtered = sidebar_filter(filtered, "יזם", C["sponsor"])
filtered = sidebar_filter(filtered, "סוג מימון", C["funding_type"])
filtered = sidebar_filter(filtered, "סוג מחקר", C["study_type"])
filtered = sidebar_filter(filtered, "רמזור ניהולי", "רמזור ניהולי")
filtered = sidebar_filter(filtered, "סטטוס ניצול תקציב", "סטטוס ניצול תקציב - מחושב")
filtered = sidebar_filter(filtered, "סטטוס גיוס", "סטטוס גיוס")


# ============================================================
# KPI ראשיים
# ============================================================

st.markdown("---")

k1, k2, k3, k4 = st.columns(4)
k1.metric("סה״כ מחקרים", number(count_unique_studies(filtered, C["unique_study"], C["study_id"])))
k2.metric("מספר חוקרים", number(filtered[C["pi"]].nunique() if C["pi"] else 0))
k3.metric("מספר מחלקות", number(filtered[C["department"]].nunique() if C["department"] else 0))
k4.metric("מספר יזמים", number(filtered[C["sponsor"]].nunique() if C["sponsor"] else 0))

k5, k6, k7, k8 = st.columns(4)
k5.metric("צפי הכנסות", money(sum_col(filtered, C["expected_income"])))
k6.metric("הכנסות בפועל", money(sum_col(filtered, C["actual_income"])))
k7.metric("סך הוצאות", money(sum_col(filtered, C["total_expenses"])))
k8.metric("תקורה", money(sum_col(filtered, C["overhead"])))


# ============================================================
# טאבים / גליונות הדשבורד
# ============================================================

tabs = st.tabs([
    "🏥 כלל בית החולים",
    "🏢 מחלקות",
    "👩‍⚕️ חוקרים",
    "🏭 יזמים",
    "🚦 סטטוס ניהול תקציב",
    "🧾 גיליון לחוקר",
    "💳 גיליון לחוקר - מעקב דרישות תשלום",
])


# ============================================================
# 1. כלל בית החולים
# ============================================================

with tabs[0]:
    st.header("🏥 כלל בית החולים")

    if C["approval_year"]:
        if C["unique_study"]:
            yearly = (
                filtered.groupby(C["approval_year"], as_index=False)[C["unique_study"]]
                .sum()
                .rename(columns={C["approval_year"]: "שנה", C["unique_study"]: "מספר מחקרים"})
            )
        else:
            yearly = (
                filtered.groupby(C["approval_year"], as_index=False)
                .size()
                .rename(columns={C["approval_year"]: "שנה", "size": "מספר מחקרים"})
            )

        plot_bar(yearly, "שנה", "מספר מחקרים", "סה״כ מחקרים בכל שנה")

    if C["approval_year"] and C["funding_type"]:
        if C["unique_study"]:
            funding = (
                filtered.groupby([C["approval_year"], C["funding_type"]], as_index=False)[C["unique_study"]]
                .sum()
                .rename(columns={C["approval_year"]: "שנה", C["funding_type"]: "סוג מימון", C["unique_study"]: "מספר מחקרים"})
            )
        else:
            funding = (
                filtered.groupby([C["approval_year"], C["funding_type"]], as_index=False)
                .size()
                .rename(columns={C["approval_year"]: "שנה", C["funding_type"]: "סוג מימון", "size": "מספר מחקרים"})
            )

        fig = px.bar(funding, x="שנה", y="מספר מחקרים", color="סוג מימון", barmode="group", text="מספר מחקרים", title="מחקרים לפי שנה וסוג מימון")
        fig.update_layout(title_x=0.5, height=500)
        st.plotly_chart(fig, use_container_width=True)

    if C["approval_year"]:
        yearly_money_cols = [C["expected_income"], C["actual_income"], C["total_expenses"], C["overhead"]]
        yearly_money_cols = [c for c in yearly_money_cols if c]
        if yearly_money_cols:
            yearly_money = filtered.groupby(C["approval_year"], as_index=False)[yearly_money_cols].sum()
            yearly_money = yearly_money.rename(columns={C["approval_year"]: "שנה"})
            plot_grouped_bar(yearly_money, "שנה", yearly_money_cols, "צפי הכנסות, הכנסות בפועל, הוצאות ותקורה לפי שנה")

    expense_cols = [
        C["salary_expenses"], C["materials_expenses"], C["fixed_expenses"],
        C["travel_expenses"], C["internal_expenses"]
    ]
    expense_cols = [c for c in expense_cols if c]

    if C["approval_year"] and expense_cols:
        exp = filtered.groupby(C["approval_year"], as_index=False)[expense_cols].sum()
        exp = exp.rename(columns={C["approval_year"]: "שנה"})
        fig = px.bar(exp, x="שנה", y=expense_cols, barmode="stack", title="התפלגות הוצאות לפי שנה")
        fig.update_layout(title_x=0.5, height=500)
        st.plotly_chart(fig, use_container_width=True)

    if C["pi"] and C["unique_study"]:
        top_pi_count = (
            filtered.groupby(C["pi"], as_index=False)[C["unique_study"]]
            .sum()
            .sort_values(C["unique_study"], ascending=False)
            .head(10)
            .rename(columns={C["pi"]: "חוקר ראשי", C["unique_study"]: "מספר מחקרים"})
        )
        plot_bar(top_pi_count, "חוקר ראשי", "מספר מחקרים", "Top 10 חוקרים לפי כמות מחקרים", horizontal=True)

    if C["pi"] and C["expected_income"]:
        top_pi_income = (
            filtered.groupby(C["pi"], as_index=False)[C["expected_income"]]
            .sum()
            .sort_values(C["expected_income"], ascending=False)
            .head(10)
            .rename(columns={C["pi"]: "חוקר ראשי", C["expected_income"]: "צפי הכנסות"})
        )
        plot_bar(top_pi_income, "חוקר ראשי", "צפי הכנסות", "Top 10 חוקרים לפי צפי הכנסות", horizontal=True)

    if C["pi"] and C["unique_study"]:
        researcher_counts = (
            filtered.groupby(C["pi"], as_index=False)[C["unique_study"]]
            .sum()
            .rename(columns={C["unique_study"]: "מספר מחקרים"})
        )

        researcher_counts["טווח מחקרים לחוקר"] = pd.cut(
            researcher_counts["מספר מחקרים"],
            bins=[0, 5, 10, 20, 50, np.inf],
            labels=["1-5", "6-10", "11-20", "21-50", "50+"],
            include_lowest=True
        )

        dist = (
            researcher_counts.groupby("טווח מחקרים לחוקר", as_index=False)
            .size()
            .rename(columns={"size": "מספר חוקרים"})
        )

        plot_bar(dist, "טווח מחקרים לחוקר", "מספר חוקרים", "התפלגות כמות מחקרים לחוקר")


# ============================================================
# 2. מחלקות
# ============================================================

with tabs[1]:
    st.header("🏢 מחלקות")

    if C["department"]:
        selected_department = st.selectbox(
            "בחרי מחלקה",
            sorted(df[C["department"]].dropna().astype(str).unique())
        )

        dept_df = df[df[C["department"]].astype(str) == selected_department]

        if C["approval_year"]:
            years = sorted(dept_df[C["approval_year"]].dropna().astype(str).unique())
            selected_years = st.multiselect("בחרי שנה / שנים", years, default=years)
            if selected_years:
                dept_df = dept_df[dept_df[C["approval_year"]].astype(str).isin(selected_years)]

        d1, d2, d3, d4 = st.columns(4)
        d1.metric("מספר מחקרים", number(count_unique_studies(dept_df, C["unique_study"], C["study_id"])))
        d2.metric("צפי הכנסות", money(sum_col(dept_df, C["expected_income"])))
        d3.metric("הכנסות בפועל", money(sum_col(dept_df, C["actual_income"])))
        d4.metric("סך הוצאות", money(sum_col(dept_df, C["total_expenses"])))

        if C["approval_year"]:
            cols = [C["expected_income"], C["actual_income"], C["total_expenses"]]
            cols = [c for c in cols if c]
            if cols:
                summary = dept_df.groupby(C["approval_year"], as_index=False)[cols].sum()
                summary = summary.rename(columns={C["approval_year"]: "שנה"})
                plot_grouped_bar(summary, "שנה", cols, "הכנסות והוצאות לפי שנה במחלקה")

        if C["approval_year"] and C["expected_participants"] and C["actual_participants"]:
            participants = (
                dept_df.groupby(C["approval_year"], as_index=False)[[C["expected_participants"], C["actual_participants"]]]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )
            plot_grouped_bar(participants, "שנה", [C["expected_participants"], C["actual_participants"]], "צפי משתתפים מול משתתפים בפועל")

        st.subheader("טבלת מחקרים במחלקה")
        st.dataframe(dept_df, use_container_width=True)


# ============================================================
# 3. חוקרים
# ============================================================

with tabs[2]:
    st.header("👩‍⚕️ חוקרים")

    if C["pi"]:
        selected_pi = st.selectbox(
            "בחרי חוקר ראשי",
            sorted(df[C["pi"]].dropna().astype(str).unique()),
            key="researcher_main"
        )

        pi_df = df[df[C["pi"]].astype(str) == selected_pi]

        if C["approval_year"]:
            years = sorted(pi_df[C["approval_year"]].dropna().astype(str).unique())
            selected_years = st.multiselect("בחרי שנה / שנים לחוקר", years, default=years)
            if selected_years:
                pi_df = pi_df[pi_df[C["approval_year"]].astype(str).isin(selected_years)]

        p1, p2, p3, p4 = st.columns(4)
        p1.metric("מספר מחקרים", number(count_unique_studies(pi_df, C["unique_study"], C["study_id"])))
        p2.metric("צפי הכנסות", money(sum_col(pi_df, C["expected_income"])))
        p3.metric("הכנסות בפועל", money(sum_col(pi_df, C["actual_income"])))
        p4.metric("סך הוצאות", money(sum_col(pi_df, C["total_expenses"])))

        if C["approval_year"]:
            cols = [C["expected_income"], C["actual_income"], C["total_expenses"]]
            cols = [c for c in cols if c]
            if cols:
                summary = pi_df.groupby(C["approval_year"], as_index=False)[cols].sum()
                summary = summary.rename(columns={C["approval_year"]: "שנה"})
                plot_grouped_bar(summary, "שנה", cols, "הכנסות מול הוצאות לפי שנה לחוקר")

        expense_cols = [
            C["salary_expenses"], C["materials_expenses"], C["fixed_expenses"],
            C["travel_expenses"], C["internal_expenses"]
        ]
        expense_cols = [c for c in expense_cols if c]

        if C["approval_year"] and expense_cols:
            exp = pi_df.groupby(C["approval_year"], as_index=False)[expense_cols].sum()
            exp = exp.rename(columns={C["approval_year"]: "שנה"})
            fig = px.bar(exp, x="שנה", y=expense_cols, barmode="stack", title="התפלגות הוצאות לפי שנה לחוקר")
            fig.update_layout(title_x=0.5, height=500)
            st.plotly_chart(fig, use_container_width=True)

        if C["approval_year"] and C["expected_participants"] and C["actual_participants"]:
            participants = (
                pi_df.groupby(C["approval_year"], as_index=False)[[C["expected_participants"], C["actual_participants"]]]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )
            plot_grouped_bar(participants, "שנה", [C["expected_participants"], C["actual_participants"]], "צפי משתתפים מול משתתפים בפועל לחוקר")

        st.subheader("טבלת מחקרים לחוקר")
        st.dataframe(pi_df, use_container_width=True)


# ============================================================
# 4. יזמים
# ============================================================

with tabs[3]:
    st.header("🏭 יזמים")

    if C["sponsor"]:
        selected_sponsors = st.multiselect(
            "בחרי יזם / יזמים",
            sorted(df[C["sponsor"]].dropna().astype(str).unique())
        )

        sponsor_df = df.copy()
        if selected_sponsors:
            sponsor_df = sponsor_df[sponsor_df[C["sponsor"]].astype(str).isin(selected_sponsors)]

        if C["approval_year"]:
            years = sorted(sponsor_df[C["approval_year"]].dropna().astype(str).unique())
            selected_years = st.multiselect("בחרי שנה / שנים ליזמים", years, default=years)
            if selected_years:
                sponsor_df = sponsor_df[sponsor_df[C["approval_year"]].astype(str).isin(selected_years)]

        if C["unique_study"]:
            sponsor_count = (
                sponsor_df.groupby(C["sponsor"], as_index=False)[C["unique_study"]]
                .sum()
                .sort_values(C["unique_study"], ascending=False)
                .rename(columns={C["sponsor"]: "יזם", C["unique_study"]: "מספר מחקרים"})
            )
        else:
            sponsor_count = (
                sponsor_df.groupby(C["sponsor"], as_index=False)
                .size()
                .sort_values("size", ascending=False)
                .rename(columns={C["sponsor"]: "יזם", "size": "מספר מחקרים"})
            )

        top_count = sponsor_count.head(10)
        other_count = sponsor_count.iloc[10:]["מספר מחקרים"].sum()
        if other_count > 0:
            top_count = pd.concat([top_count, pd.DataFrame({"יזם": ["אחר"], "מספר מחקרים": [other_count]})], ignore_index=True)

        plot_pie(top_count, "יזם", "מספר מחקרים", "התפלגות כמות מחקרים לפי יזם - Top 10 ואחר")
        plot_bar(sponsor_count.head(10), "יזם", "מספר מחקרים", "Top 10 יזמים לפי כמות מחקרים", horizontal=True)

        if C["expected_income"]:
            sponsor_income = (
                sponsor_df.groupby(C["sponsor"], as_index=False)[C["expected_income"]]
                .sum()
                .sort_values(C["expected_income"], ascending=False)
                .rename(columns={C["sponsor"]: "יזם", C["expected_income"]: "צפי הכנסות"})
            )

            top_income = sponsor_income.head(10)
            other_income = sponsor_income.iloc[10:]["צפי הכנסות"].sum()
            if other_income > 0:
                top_income = pd.concat([top_income, pd.DataFrame({"יזם": ["אחר"], "צפי הכנסות": [other_income]})], ignore_index=True)

            plot_pie(top_income, "יזם", "צפי הכנסות", "התפלגות צפי הכנסות לפי יזם - Top 10 ואחר")
            plot_bar(sponsor_income.head(10), "יזם", "צפי הכנסות", "Top 10 יזמים לפי צפי הכנסות", horizontal=True)

        st.subheader("טבלת יזמים")
        st.dataframe(sponsor_df, use_container_width=True)


# ============================================================
# 5. סטטוס ניהול תקציב
# ============================================================

with tabs[4]:
    st.header("🚦 סטטוס ניהול תקציב")

    status_summary = (
        filtered.groupby("סטטוס ניצול תקציב - מחושב", as_index=False)
        .size()
        .rename(columns={"size": "מספר מחקרים"})
    )
    plot_bar(status_summary, "סטטוס ניצול תקציב - מחושב", "מספר מחקרים", "סטטוס ניצול תקציבי")

    traffic_summary = (
        filtered.groupby("רמזור ניהולי", as_index=False)
        .size()
        .rename(columns={"size": "מספר מחקרים"})
    )
    plot_bar(traffic_summary, "רמזור ניהולי", "מספר מחקרים", "רמזור ניהולי")

    st.subheader("🔴 מחקרים בחריגה")
    st.dataframe(filtered[filtered["סטטוס ניצול תקציב - מחושב"] == "חריגה"], use_container_width=True)

    st.subheader("🟡 מחקרים קרובים לניצול מלא")
    st.dataframe(filtered[filtered["סטטוס ניצול תקציב - מחושב"] == "קרוב לניצול מלא"], use_container_width=True)

    st.subheader("🟡 מחקרים בניצול נמוך")
    st.dataframe(filtered[filtered["סטטוס ניצול תקציב - מחושב"] == "ניצול נמוך"], use_container_width=True)

    st.subheader("🟡 מחקרים עם גיוס משתתפים נמוך / ללא גיוס")
    st.dataframe(filtered[filtered["סטטוס גיוס"].isin(["אין גיוס", "גיוס נמוך"])], use_container_width=True)

    st.subheader("🟡 מחקרים שמסתיימים תוך חודשיים")
    st.dataframe(filtered[(filtered["ימים לסיום"] >= 0) & (filtered["ימים לסיום"] <= 60)], use_container_width=True)


# ============================================================
# 6. גיליון לחוקר
# ============================================================

with tabs[5]:
    st.header("🧾 גיליון לחוקר")

    if C["pi"]:
        researcher = st.selectbox(
            "בחרי חוקר להצגת גיליון אישי",
            sorted(df[C["pi"]].dropna().astype(str).unique()),
            key="researcher_personal"
        )

        r_df = df[df[C["pi"]].astype(str) == researcher]

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("מספר מחקרים", number(count_unique_studies(r_df, C["unique_study"], C["study_id"])))
        r2.metric("תקציב כולל", money(sum_col(r_df, C["budget"])))
        r3.metric("סה״כ ניצול", money(sum_col(r_df, C["utilization_total"])))
        r4.metric("יתרה לניצול", money(sum_col(r_df, C["balance"])))

        r5, r6, r7, r8 = st.columns(4)
        r5.metric("צפי הכנסות", money(sum_col(r_df, C["expected_income"])))
        r6.metric("הכנסות בפועל", money(sum_col(r_df, C["actual_income"])))
        r7.metric("סך הוצאות", money(sum_col(r_df, C["total_expenses"])))
        r8.metric("ממוצע ניצול תקציבי", pct(r_df["% ניצול תקציב - מחושב"].mean()))

        st.subheader("רשימת תקציבים / מחקרים של החוקר")

        cols_for_researcher = [
            C["wbs"], C["budget_name"], C["pi"], C["budget_owner"], C["study_id"],
            C["protocol"], C["site"], C["contract"], C["start_date"], C["end_date"],
            C["sponsor"], C["research_class"], C["country"], C["budget"], C["execution"],
            C["commitment"], C["utilization_total"], C["balance"], C["unreserved_balance"],
            "% ניצול תקציב - מחושב", "סטטוס ניצול תקציב - מחושב", "רמזור ניהולי",
            "% גיוס משתתפים", "סטטוס גיוס", "ימים לסיום"
        ]
        cols_for_researcher = [c for c in cols_for_researcher if c and c in r_df.columns]

        st.dataframe(r_df[cols_for_researcher], use_container_width=True)

        if C["study_id"]:
            st.subheader("תעודת זהות למחקר")
            selected_study = st.selectbox(
                "בחרי מחקר של החוקר",
                sorted(r_df[C["study_id"]].dropna().astype(str).unique())
            )

            study_df = r_df[r_df[C["study_id"]].astype(str) == selected_study]
            if not study_df.empty:
                row = study_df.iloc[0]

                a, b, c = st.columns(3)
                a.metric("מספר הלסינקי", str(row.get(C["study_id"], "")))
                b.metric("מספר פרוטוקול", str(row.get(C["protocol"], "")) if C["protocol"] else "")
                c.metric("רמזור", str(row.get("רמזור ניהולי", "")))

                d, e, f = st.columns(3)
                d.metric("יזם", str(row.get(C["sponsor"], "")) if C["sponsor"] else "")
                e.metric("תקציב", money(row.get(C["budget"], 0)) if C["budget"] else "0 ₪")
                f.metric("% ניצול", pct(row.get("% ניצול תקציב - מחושב", 0)))

                st.dataframe(study_df, use_container_width=True)

        researcher_excel = download_excel({"גיליון לחוקר": r_df[cols_for_researcher] if cols_for_researcher else r_df})
        st.download_button(
            "⬇️ הורדת גיליון החוקר לאקסל",
            data=researcher_excel,
            file_name="researcher_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


# ============================================================
# 7. גיליון לחוקר - מעקב דרישות תשלום
# ============================================================

with tabs[6]:
    st.header("💳 גיליון לחוקר - מעקב דרישות תשלום")
    st.write("מעקב אחר ההכנסות, ההוצאות, התקציב, הביצוע, ההתחייבויות והיתרה של המחקרים לפי גיליון הפירוט.")

    if C["pi"]:
        researcher_payment = st.selectbox(
            "בחרי חוקר",
            sorted(df[C["pi"]].dropna().astype(str).unique()),
            key="researcher_payments"
        )

        researcher_studies = df[df[C["pi"]].astype(str) == researcher_payment]

        study_ids = []
        protocols = []

        if C["study_id"]:
            study_ids = researcher_studies[C["study_id"]].dropna().astype(str).unique().tolist()

        if C["protocol"]:
            protocols = researcher_studies[C["protocol"]].dropna().astype(str).unique().tolist()

        details_researcher = details.copy()

        filters = []

        if D["study_id"] and study_ids:
            filters.append(details_researcher[D["study_id"]].astype(str).isin(study_ids))

        if D["protocol"] and protocols:
            filters.append(details_researcher[D["protocol"]].astype(str).isin(protocols))

        if D["pi_name"]:
            filters.append(details_researcher[D["pi_name"]].astype(str) == str(researcher_payment))

        if filters:
            combined_filter = filters[0]
            for f in filters[1:]:
                combined_filter = combined_filter | f
            details_researcher = details_researcher[combined_filter]

        p1, p2, p3, p4 = st.columns(4)
        p1.metric("סה״כ תקציב", money(sum_col(details_researcher, D["budget_total"])))
        p2.metric("התחייבויות רכש", money(sum_col(details_researcher, D["purchase_commitments"])))
        p3.metric("סה״כ ביצוע", money(sum_col(details_researcher, D["execution_total"])))
        p4.metric("יתרה לניצול", money(sum_col(details_researcher, D["balance"])))

        if D["budget_category"]:
            summary = (
                details_researcher.groupby(D["budget_category"], as_index=False)[
                    [c for c in [D["budget_total"], D["purchase_commitments"], D["execution_total"], D["balance"]] if c]
                ]
                .sum()
                .rename(columns={D["budget_category"]: "קטגוריית סעיף תקציבי"})
            )

            st.subheader("סיכום לפי קטגוריית סעיף תקציבי")
            st.dataframe(summary, use_container_width=True)

            plot_grouped_bar(
                summary,
                "קטגוריית סעיף תקציבי",
                [D["budget_total"], D["purchase_commitments"], D["execution_total"], D["balance"]],
                "תקציב, התחייבויות, ביצוע ויתרה לפי קטגוריה"
            )

        if D["study_id"] and not details_researcher.empty:
            selected_payment_study = st.selectbox(
                "בחרי מחקר לפירוט",
                sorted(details_researcher[D["study_id"]].dropna().astype(str).unique())
            )

            details_study = details_researcher[details_researcher[D["study_id"]].astype(str) == selected_payment_study]

            s1, s2, s3, s4 = st.columns(4)
            s1.metric("תקציב למחקר", money(sum_col(details_study, D["budget_total"])))
            s2.metric("התחייבויות למחקר", money(sum_col(details_study, D["purchase_commitments"])))
            s3.metric("ביצוע למחקר", money(sum_col(details_study, D["execution_total"])))
            s4.metric("יתרה למחקר", money(sum_col(details_study, D["balance"])))

            st.subheader("פירוט הוצאות והכנסות למחקר")
            st.dataframe(details_study, use_container_width=True)

        st.subheader("טבלת מעקב מלאה לחוקר")
        st.dataframe(details_researcher, use_container_width=True)

        payments_excel = download_excel({
            "מעקב דרישות תשלום": details_researcher
        })

        st.download_button(
            "⬇️ הורדת מעקב דרישות תשלום לאקסל",
            data=payments_excel,
            file_name="researcher_payment_tracking.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


# ============================================================
# הורדת כל הדאטה
# ============================================================

st.sidebar.markdown("---")
st.sidebar.header("⬇️ הורדות")

export_file = download_excel({
    "filtered_studies": filtered,
    "details": details,
    "original_studies": studies_df
})

st.sidebar.download_button(
    "הורדת כל הדאטה המסונן לאקסל",
    data=export_file,
    file_name="clinical_research_dashboard_export.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.sidebar.caption("Clinical Research Dashboard | Streamlit")