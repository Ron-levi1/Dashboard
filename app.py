import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

# ============================================================
# App config
# ============================================================
st.set_page_config(
    page_title="דשבורד מחקרים קליניים",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_VERSION = "v2-clean-tabs-no-sidebar-2026-06-08"

# ============================================================
# CSS - RTL + cleaner dashboard design
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
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }
    h1, h2, h3, h4, h5, h6, p, label, span {
        text-align: right;
        direction: rtl;
    }
    section[data-testid="stSidebar"] {display: none;}
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #dbe3ef;
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
    }
    div[data-testid="stMetricLabel"] {font-size: 0.95rem; color: #475569;}
    div[data-testid="stMetricValue"] {font-size: 1.45rem; font-weight: 800; color: #0f172a;}
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #0e7490 100%);
        color: white;
        padding: 28px 30px;
        border-radius: 24px;
        margin-bottom: 18px;
        box-shadow: 0 12px 35px rgba(15, 23, 42, 0.18);
    }
    .hero h1 {color: white; margin: 0 0 8px 0; font-size: 2.15rem;}
    .hero p {color: #dbeafe; margin: 0; font-size: 1.05rem;}
    .filter-card {
        background: #f8fafc;
        border: 1px solid #dbe3ef;
        border-radius: 18px;
        padding: 14px 16px;
        margin-bottom: 16px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8fafc;
        border-radius: 16px;
        padding: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: #ffffff;
        border-radius: 14px;
        padding: 10px 16px;
        border: 1px solid #e2e8f0;
        font-weight: 700;
    }
    .stTabs [aria-selected="true"] {
        background: #dbeafe !important;
        border-color: #60a5fa !important;
        color: #0f172a !important;
    }
    [data-testid="stDataFrame"] {direction: rtl; text-align: right;}
    [data-testid="stDataFrame"] * {direction: rtl; text-align: right;}
    div[data-testid="stSelectbox"] label,
    div[data-testid="stMultiSelect"] label {
        font-weight: 700;
        color: #1e293b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Helper functions
# ============================================================

def normalize_text(value):
    if pd.isna(value):
        return ""
    value = str(value)
    value = value.replace("\u200f", "").replace("\u200e", "")
    value = value.replace("–", "-").replace("—", "-").replace("−", "-")
    value = value.replace("״", '"').replace("”", '"').replace("“", '"')
    return " ".join(value.split()).strip()


def normalize_columns(df):
    df = df.copy()
    df.columns = [normalize_text(c) for c in df.columns]
    return df


def find_col(df, candidates):
    mapping = {normalize_text(c): c for c in df.columns}
    for candidate in candidates:
        key = normalize_text(candidate)
        if key in mapping:
            return mapping[key]
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


def count_unique_studies(df, unique_col=None, study_id_col=None):
    if unique_col and unique_col in df.columns:
        s = to_numeric(df[unique_col]).sum()
        if s > 0:
            return s

    if study_id_col and study_id_col in df.columns:
        return df[study_id_col].dropna().astype(str).nunique()

    return len(df)


def download_excel_openpyxl(sheets_dict):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, data in sheets_dict.items():
            safe_name = str(sheet_name)[:31]
            if data is None:
                data = pd.DataFrame()
            data.to_excel(writer, index=False, sheet_name=safe_name)
    return output.getvalue()


def display_df(data, height=420):
    if data is None or data.empty:
        st.info("אין נתונים להצגה בהתאם לבחירה הנוכחית.")
        return

    styled = data.style.set_properties(**{"text-align": "right", "direction": "rtl"})
    st.dataframe(styled, use_container_width=True, height=height)


def budget_status(value):
    try:
        value = float(value)
    except Exception:
        return "לא ידוע"

    if value < 20:
        return "ניצול נמוך"
    if value <= 80:
        return "תקין"
    if value <= 100:
        return "קרוב לניצול מלא"
    return "חריגה"


def recruitment_status(value):
    try:
        value = float(value)
    except Exception:
        return "לא ידוע"

    if value == 0:
        return "אין גיוס"
    if value < 50:
        return "גיוס נמוך"
    if value < 80:
        return "גיוס בינוני"
    return "גיוס תקין"


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


def filter_multiselect(df, label, col, default_all=True, key=None):
    if not col or col not in df.columns:
        return df

    values = sorted(df[col].dropna().astype(str).unique())
    default = values if default_all else []

    selected = st.multiselect(label, values, default=default, key=key)

    if selected:
        return df[df[col].astype(str).isin(selected)]

    return df.iloc[0:0]


def filter_select(df, label, col, key=None):
    if not col or col not in df.columns:
        return df, None

    values = sorted(df[col].dropna().astype(str).unique())

    if not values:
        return df.iloc[0:0], None

    selected = st.selectbox(label, values, key=key)

    return df[df[col].astype(str) == selected], selected


def plot_bar(data, x, y, title, horizontal=False):
    if data is None or data.empty or x not in data.columns or y not in data.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    if horizontal:
        fig = px.bar(data, x=y, y=x, orientation="h", text=y, title=title)
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
    else:
        fig = px.bar(data, x=x, y=y, text=y, title=title)

    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig.update_layout(
        title_x=0.5,
        height=460,
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_grouped_bar(data, x, y_cols, title):
    y_cols = [c for c in y_cols if c and c in data.columns]

    if data is None or data.empty or x not in data.columns or not y_cols:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    fig = px.bar(data, x=x, y=y_cols, barmode="group", title=title)
    fig.update_layout(
        title_x=0.5,
        height=460,
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_pie(data, names, values, title):
    if data is None or data.empty or names not in data.columns or values not in data.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    fig = px.pie(data, names=names, values=values, hole=0.4, title=title)
    fig.update_layout(title_x=0.5, height=460, paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)


def top10_plus_other(data, group_col, value_col, group_name, value_name):
    if not group_col or not value_col or group_col not in data.columns or value_col not in data.columns:
        return pd.DataFrame()

    temp = data.copy()
    temp[value_col] = to_numeric(temp[value_col])

    grouped = (
        temp.groupby(group_col, as_index=False)[value_col]
        .sum()
        .sort_values(value_col, ascending=False)
        .rename(columns={group_col: group_name, value_col: value_name})
    )

    top10 = grouped.head(10)
    other_sum = grouped.iloc[10:][value_name].sum()

    if other_sum > 0:
        top10 = pd.concat(
            [top10, pd.DataFrame({group_name: ["אחר"], value_name: [other_sum]})],
            ignore_index=True,
        )

    return top10


def show_kpis(items):
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        col.metric(label, value)


def find_studies_sheet(xls):
    names = xls.sheet_names

    for name in names:
        if normalize_text(name).lower() == "studies_data":
            return name

    return names[0]


def find_details_sheet(xls, studies_sheet):
    for name in xls.sheet_names:
        if name == studies_sheet:
            continue

        sample = normalize_columns(pd.read_excel(xls, sheet_name=name, nrows=5))

        if find_col(sample, ["קטגוריית סעיף תקציבי"]) or find_col(sample, ["מספר הלסינקי"]):
            return name

    other_sheets = [s for s in xls.sheet_names if s != studies_sheet]

    if other_sheets:
        return other_sheets[0]

    return studies_sheet


# ============================================================
# Header + Upload
# ============================================================

st.markdown(
    f"""
    <div class="hero">
        <h1>📊 דשבורד ניהולי למחקרים קליניים</h1>
        <p>העלי קובץ Excel, והדשבורד ייפתח אוטומטית לפי הגיליונות והעמודות שהוגדרו. גרסה: {APP_VERSION}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader("העלי קובץ Excel", type=["xlsx"])

if uploaded_file is None:
    st.info("יש להעלות קובץ Excel כדי להתחיל.")
    st.stop()

try:
    xls = pd.ExcelFile(uploaded_file)
    studies_sheet = find_studies_sheet(xls)
    details_sheet = find_details_sheet(xls, studies_sheet)

    studies_df = normalize_columns(pd.read_excel(xls, sheet_name=studies_sheet))
    details_df = normalize_columns(pd.read_excel(xls, sheet_name=details_sheet))

except Exception as e:
    st.error("לא הצלחתי לקרוא את קובץ האקסל.")
    st.exception(e)
    st.stop()

with st.expander("מידע טכני על הקובץ", expanded=False):
    st.write("גיליון מחקרים שזוהה:", studies_sheet)
    st.write("גיליון פירוט שזוהה:", details_sheet)
    st.write("כל הגיליונות בקובץ:", xls.sheet_names)


# ============================================================
# Column mapping
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
    "study_type": find_col(studies_df, ["סוג המחקר"]),
    "phase": find_col(studies_df, ["פאזת המחקר", "פאזה"]),
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
    "unreserved_balance": find_col(studies_df, ["יתרה לא משוריינת"]),
    "research_class": find_col(studies_df, ["סיווג מחקר (תקן 40)- סוג פרויקט", "סיווג מחקר (תקן 40) - סוג פרויקט", "סוג פרויקט"]),
    "gl_account": find_col(studies_df, ["חשבון GL"]),
    "gl_name": find_col(studies_df, ["שם חשבון GL"]),
}

D = {
    "wbs": find_col(details_df, ["אלמנט WBS", "מספר WBS"]),
    "commitment_group": find_col(details_df, ["קבוצת פריט התחייבות"]),
    "commitment_group_desc": find_col(details_df, ["תיאור קבוצת פריט התחייבות"]),
    "pi_name": find_col(details_df, ["שם חוקר ראשי", "חוקר ראשי"]),
    "protocol": find_col(details_df, ["מספר פרוטוקול"]),
    "study_id": find_col(details_df, ["מספר הלסינקי"]),
    "site": find_col(details_df, ["site", "SITE"]),
    "budget_category": find_col(details_df, ["קטגוריית סעיף תקציבי"]),
    "description": find_col(details_df, ["תיאור"]),
    "budget_total": find_col(details_df, ["סה\"כ תקציב מ", "סהכ תקציב מ"]),
    "purchase_commitments": find_col(details_df, ["התחייבויות רכש"]),
    "execution_total": find_col(details_df, ["סה\"כ ביצוע", "סהכ ביצוע"]),
    "balance": find_col(details_df, ["יתרה לניצול"]),
}

numeric_studies_cols = [
    C["expected_income"],
    C["actual_income"],
    C["total_expenses"],
    C["salary_expenses"],
    C["materials_expenses"],
    C["fixed_expenses"],
    C["travel_expenses"],
    C["internal_expenses"],
    C["expected_participants"],
    C["actual_participants"],
    C["unique_study"],
    C["unique_researcher"],
    C["budget"],
    C["overhead"],
    C["commitment"],
    C["execution"],
    C["utilization_total"],
    C["utilization_pct"],
    C["balance"],
    C["unreserved_balance"],
]

numeric_details_cols = [
    D["budget_total"],
    D["purchase_commitments"],
    D["execution_total"],
    D["balance"],
]

df = make_numeric(studies_df, numeric_studies_cols)
details = make_numeric(details_df, numeric_details_cols)

for date_col in [C["approval_date"], C["start_date"], C["end_date"]]:
    if date_col and date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)

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
    used = to_numeric(df[C["utilization_total"]])

    df["% ניצול תקציב - מחושב"] = np.where(budget > 0, used / budget * 100, 0)

else:
    df["% ניצול תקציב - מחושב"] = 0

df["סטטוס ניצול תקציב - מחושב"] = df["% ניצול תקציב - מחושב"].apply(budget_status)

if C["expected_participants"] and C["actual_participants"]:
    expected = to_numeric(df[C["expected_participants"]])
    actual = to_numeric(df[C["actual_participants"]])

    df["% גיוס משתתפים"] = np.where(expected > 0, actual / expected * 100, 0)

else:
    df["% גיוס משתתפים"] = 0

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
        row["% גיוס משתתפים"],
    ),
    axis=1,
)


# ============================================================
# Tabs
# ============================================================

tabs = st.tabs(
    [
        "🏥 כלל בית החולים",
        "🏢 מחלקות",
        "👩‍⚕️ חוקרים",
        "🏭 יזמים",
        "🚦 סטטוס ניהול תקציב",
        "🧾 גיליון לחוקר",
        "💳 גיליון לחוקר - מעקב דרישות תשלום",
    ]
)

# ============================================================
# 1. Hospital
# ============================================================

with tabs[0]:
    st.header("🏥 כלל בית החולים")
    st.markdown('<div class="filter-card"><b>פילטרים:</b></div>', unsafe_allow_html=True)

    filtered = df.copy()

    c1, c2, c3 = st.columns(3)

    with c1:
        filtered = filter_multiselect(filtered, "שנה", C["approval_year"], key="hospital_year")

    with c2:
        filtered = filter_multiselect(filtered, "סוג מימון", C["funding_type"], key="hospital_funding")

    with c3:
        filtered = filter_multiselect(filtered, "סוג מחקר", C["study_type"], key="hospital_type")

    show_kpis(
        [
            ("סה״כ מחקרים", number(count_unique_studies(filtered, C["unique_study"], C["study_id"]))),
            ("מספר חוקרים", number(filtered[C["pi"]].nunique() if C["pi"] else 0)),
            ("צפי הכנסות", money(sum_col(filtered, C["expected_income"]))),
            ("הכנסות בפועל", money(sum_col(filtered, C["actual_income"]))),
            ("סך הוצאות", money(sum_col(filtered, C["total_expenses"]))),
        ]
    )

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

        plot_bar(yearly, "שנה", "מספר מחקרים", "סה״כ מחקרים לפי שנה")

        money_cols = [
            C["expected_income"],
            C["actual_income"],
            C["total_expenses"],
            C["overhead"],
        ]
        money_cols = [c for c in money_cols if c]

        if money_cols:
            yearly_money = (
                filtered.groupby(C["approval_year"], as_index=False)[money_cols]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )

            plot_grouped_bar(
                yearly_money,
                "שנה",
                money_cols,
                "צפי הכנסות, הכנסות בפועל, הוצאות ותקורה לפי שנה",
            )

    if C["funding_type"] and C["unique_study"]:
        funding = (
            filtered.groupby(C["funding_type"], as_index=False)[C["unique_study"]]
            .sum()
            .rename(columns={C["funding_type"]: "סוג מימון", C["unique_study"]: "מספר מחקרים"})
        )

        plot_pie(funding, "סוג מימון", "מספר מחקרים", "התפלגות מחקרים לפי סוג מימון")

    expense_cols = [
        C["salary_expenses"],
        C["materials_expenses"],
        C["fixed_expenses"],
        C["travel_expenses"],
        C["internal_expenses"],
    ]
    expense_cols = [c for c in expense_cols if c]

    if C["approval_year"] and expense_cols:
        exp = (
            filtered.groupby(C["approval_year"], as_index=False)[expense_cols]
            .sum()
            .rename(columns={C["approval_year"]: "שנה"})
        )

        fig = px.bar(exp, x="שנה", y=expense_cols, barmode="stack", title="התפלגות הוצאות לפי שנה")
        fig.update_layout(title_x=0.5, height=460)
        st.plotly_chart(fig, use_container_width=True)

    if C["pi"] and C["unique_study"]:
        top_pi = (
            filtered.groupby(C["pi"], as_index=False)[C["unique_study"]]
            .sum()
            .sort_values(C["unique_study"], ascending=False)
            .head(10)
            .rename(columns={C["pi"]: "חוקר ראשי", C["unique_study"]: "מספר מחקרים"})
        )

        plot_bar(top_pi, "חוקר ראשי", "מספר מחקרים", "Top 10 חוקרים לפי כמות מחקרים", horizontal=True)

    if C["pi"] and C["expected_income"]:
        top_income = (
            filtered.groupby(C["pi"], as_index=False)[C["expected_income"]]
            .sum()
            .sort_values(C["expected_income"], ascending=False)
            .head(10)
            .rename(columns={C["pi"]: "חוקר ראשי", C["expected_income"]: "צפי הכנסות"})
        )

        plot_bar(top_income, "חוקר ראשי", "צפי הכנסות", "Top 10 חוקרים לפי צפי הכנסות", horizontal=True)

    if C["pi"] and C["unique_study"]:
        rc = (
            filtered.groupby(C["pi"], as_index=False)[C["unique_study"]]
            .sum()
            .rename(columns={C["unique_study"]: "מספר מחקרים"})
        )

        rc["טווח מחקרים לחוקר"] = pd.cut(
            rc["מספר מחקרים"],
            bins=[0, 5, 10, 20, 50, np.inf],
            labels=["1-5", "6-10", "11-20", "21-50", "50+"],
            include_lowest=True,
        )

        dist = (
            rc.groupby("טווח מחקרים לחוקר", as_index=False)
            .size()
            .rename(columns={"size": "מספר חוקרים"})
        )

        plot_bar(dist, "טווח מחקרים לחוקר", "מספר חוקרים", "התפלגות כמות מחקרים לחוקר")


# ============================================================
# 2. Departments
# ============================================================

with tabs[1]:
    st.header("🏢 מחלקות")

    dept_df = df.copy()

    c1, c2 = st.columns(2)

    with c1:
        dept_df, selected_department = filter_select(dept_df, "מחלקה", C["department"], key="dept_department")

    with c2:
        dept_df = filter_multiselect(dept_df, "שנה", C["approval_year"], key="dept_year")

    show_kpis(
        [
            ("מחלקה", selected_department or "-"),
            ("מספר מחקרים", number(count_unique_studies(dept_df, C["unique_study"], C["study_id"]))),
            ("הכנסות בפועל", money(sum_col(dept_df, C["actual_income"]))),
            ("סך הוצאות", money(sum_col(dept_df, C["total_expenses"]))),
        ]
    )

    if C["approval_year"]:
        cols = [C["expected_income"], C["actual_income"], C["total_expenses"]]
        cols = [c for c in cols if c]

        if cols:
            summary = (
                dept_df.groupby(C["approval_year"], as_index=False)[cols]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )

            plot_grouped_bar(summary, "שנה", cols, "הכנסות והוצאות לפי שנה במחלקה")

        if C["expected_participants"] and C["actual_participants"]:
            participants = (
                dept_df.groupby(C["approval_year"], as_index=False)[
                    [C["expected_participants"], C["actual_participants"]]
                ]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )

            plot_grouped_bar(
                participants,
                "שנה",
                [C["expected_participants"], C["actual_participants"]],
                "צפי משתתפים מול משתתפים בפועל",
            )

    st.subheader("טבלת מחקרים במחלקה")
    display_df(dept_df)


# ============================================================
# 3. Researchers
# ============================================================

with tabs[2]:
    st.header("👩‍⚕️ חוקרים")

    pi_df = df.copy()

    c1, c2 = st.columns(2)

    with c1:
        pi_df, selected_pi = filter_select(pi_df, "חוקר ראשי", C["pi"], key="pi_select")

    with c2:
        pi_df = filter_multiselect(pi_df, "שנה", C["approval_year"], key="pi_year")

    show_kpis(
        [
            ("חוקר", selected_pi or "-"),
            ("מספר מחקרים", number(count_unique_studies(pi_df, C["unique_study"], C["study_id"]))),
            ("צפי הכנסות", money(sum_col(pi_df, C["expected_income"]))),
            ("סך הוצאות", money(sum_col(pi_df, C["total_expenses"]))),
        ]
    )

    if C["approval_year"]:
        cols = [C["expected_income"], C["actual_income"], C["total_expenses"]]
        cols = [c for c in cols if c]

        if cols:
            summary = (
                pi_df.groupby(C["approval_year"], as_index=False)[cols]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )

            plot_grouped_bar(summary, "שנה", cols, "הכנסות מול הוצאות לפי שנה לחוקר")

        expense_cols = [
            C["salary_expenses"],
            C["materials_expenses"],
            C["fixed_expenses"],
            C["travel_expenses"],
            C["internal_expenses"],
        ]
        expense_cols = [c for c in expense_cols if c]

        if expense_cols:
            exp = (
                pi_df.groupby(C["approval_year"], as_index=False)[expense_cols]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )

            fig = px.bar(exp, x="שנה", y=expense_cols, barmode="stack", title="התפלגות הוצאות לפי שנה לחוקר")
            fig.update_layout(title_x=0.5, height=460)
            st.plotly_chart(fig, use_container_width=True)

        if C["expected_participants"] and C["actual_participants"]:
            participants = (
                pi_df.groupby(C["approval_year"], as_index=False)[
                    [C["expected_participants"], C["actual_participants"]]
                ]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )

            plot_grouped_bar(
                participants,
                "שנה",
                [C["expected_participants"], C["actual_participants"]],
                "צפי משתתפים מול משתתפים בפועל",
            )

    st.subheader("טבלת מחקרים לחוקר")
    display_df(pi_df)


# ============================================================
# 4. Sponsors
# ============================================================

with tabs[3]:
    st.header("🏭 יזמים")

    sponsor_df = df.copy()

    c1, c2 = st.columns(2)

    with c1:
        sponsor_df = filter_multiselect(sponsor_df, "יזם", C["sponsor"], key="sponsor_select")

    with c2:
        sponsor_df = filter_multiselect(sponsor_df, "שנה", C["approval_year"], key="sponsor_year")

    if C["sponsor"]:
        if C["unique_study"]:
            count_data = (
                sponsor_df.groupby(C["sponsor"], as_index=False)[C["unique_study"]]
                .sum()
                .sort_values(C["unique_study"], ascending=False)
                .rename(columns={C["sponsor"]: "יזם", C["unique_study"]: "מספר מחקרים"})
            )
        else:
            count_data = (
                sponsor_df.groupby(C["sponsor"], as_index=False)
                .size()
                .sort_values("size", ascending=False)
                .rename(columns={C["sponsor"]: "יזם", "size": "מספר מחקרים"})
            )

        top_count = count_data.head(10)
        other = count_data.iloc[10:]["מספר מחקרים"].sum()

        if other > 0:
            top_count = pd.concat(
                [top_count, pd.DataFrame({"יזם": ["אחר"], "מספר מחקרים": [other]})],
                ignore_index=True,
            )

        plot_pie(top_count, "יזם", "מספר מחקרים", "התפלגות כמות מחקרים לפי יזם - Top 10 ואחר")
        plot_bar(count_data.head(10), "יזם", "מספר מחקרים", "Top 10 יזמים לפי כמות מחקרים", horizontal=True)

    if C["sponsor"] and C["expected_income"]:
        income_data = (
            sponsor_df.groupby(C["sponsor"], as_index=False)[C["expected_income"]]
            .sum()
            .sort_values(C["expected_income"], ascending=False)
            .rename(columns={C["sponsor"]: "יזם", C["expected_income"]: "צפי הכנסות"})
        )

        top_income = income_data.head(10)
        other_income = income_data.iloc[10:]["צפי הכנסות"].sum()

        if other_income > 0:
            top_income = pd.concat(
                [top_income, pd.DataFrame({"יזם": ["אחר"], "צפי הכנסות": [other_income]})],
                ignore_index=True,
            )

        plot_pie(top_income, "יזם", "צפי הכנסות", "התפלגות צפי הכנסות לפי יזם - Top 10 ואחר")
        plot_bar(income_data.head(10), "יזם", "צפי הכנסות", "Top 10 יזמים לפי צפי הכנסות", horizontal=True)

    st.subheader("טבלת יזמים")
    display_df(sponsor_df)


# ============================================================
# 5. Budget status
# ============================================================

with tabs[4]:
    st.header("🚦 סטטוס ניהול תקציב")

    status_df = df.copy()

    c1, c2, c3 = st.columns(3)

    with c1:
        status_df = filter_multiselect(status_df, "שנה", C["approval_year"], key="status_year")

    with c2:
        status_df = filter_multiselect(status_df, "מחלקה", C["department"], key="status_dept")

    with c3:
        status_df = filter_multiselect(status_df, "חוקר ראשי", C["pi"], key="status_pi")

    c4, c5, c6 = st.columns(3)

    with c4:
        status_df = filter_multiselect(status_df, "סטטוס ניצול", "סטטוס ניצול תקציב - מחושב", key="status_util")

    with c5:
        status_df = filter_multiselect(status_df, "רמזור", "רמזור ניהולי", key="status_light")

    with c6:
        status_df = filter_multiselect(status_df, "סטטוס גיוס", "סטטוס גיוס", key="status_recruit")

    show_kpis(
        [
            ("מחקרים בחריגה", number((status_df["סטטוס ניצול תקציב - מחושב"] == "חריגה").sum())),
            ("קרובים לניצול מלא", number((status_df["סטטוס ניצול תקציב - מחושב"] == "קרוב לניצול מלא").sum())),
            ("ניצול נמוך", number((status_df["סטטוס ניצול תקציב - מחושב"] == "ניצול נמוך").sum())),
            ("גיוס נמוך / אין גיוס", number(status_df["סטטוס גיוס"].isin(["אין גיוס", "גיוס נמוך"]).sum())),
        ]
    )

    status_summary = (
        status_df.groupby("סטטוס ניצול תקציב - מחושב", as_index=False)
        .size()
        .rename(columns={"size": "מספר מחקרים"})
    )

    plot_bar(status_summary, "סטטוס ניצול תקציב - מחושב", "מספר מחקרים", "סטטוס ניצול תקציבי")

    traffic_summary = (
        status_df.groupby("רמזור ניהולי", as_index=False)
        .size()
        .rename(columns={"size": "מספר מחקרים"})
    )

    plot_bar(traffic_summary, "רמזור ניהולי", "מספר מחקרים", "רמזור ניהולי")

    st.subheader("טבלת סטטוס ניהול תקציב")
    display_df(status_df)


# ============================================================
# 6. Researcher sheet
# ============================================================

with tabs[5]:
    st.header("🧾 גיליון לחוקר")

    r_df = df.copy()

    c1, c2 = st.columns(2)

    with c1:
        r_df, researcher = filter_select(r_df, "חוקר", C["pi"], key="researcher_sheet_select")

    with c2:
        r_df = filter_multiselect(r_df, "שנה", C["approval_year"], key="researcher_sheet_year")

    show_kpis(
        [
            ("חוקר", researcher or "-"),
            ("מספר מחקרים", number(count_unique_studies(r_df, C["unique_study"], C["study_id"]))),
            ("תקציב כולל", money(sum_col(r_df, C["budget"]))),
            ("סה״כ ניצול", money(sum_col(r_df, C["utilization_total"]))),
            ("יתרה לניצול", money(sum_col(r_df, C["balance"]))),
        ]
    )

    cols = [
        C["wbs"],
        C["budget_name"],
        C["pi"],
        C["budget_owner"],
        C["study_id"],
        C["protocol"],
        C["site"],
        C["contract"],
        C["start_date"],
        C["end_date"],
        C["sponsor"],
        C["research_class"],
        C["country"],
        C["budget"],
        C["execution"],
        C["commitment"],
        C["utilization_total"],
        C["balance"],
        C["unreserved_balance"],
        "% ניצול תקציב - מחושב",
        "סטטוס ניצול תקציב - מחושב",
        "רמזור ניהולי",
        "% גיוס משתתפים",
        "סטטוס גיוס",
        "ימים לסיום",
    ]

    cols = [c for c in cols if c and c in r_df.columns]

    st.subheader("רשימת תקציבים / מחקרים")
    display_df(r_df[cols] if cols else r_df)

    if C["study_id"] and not r_df.empty:
        st.subheader("תעודת זהות למחקר")

        study_df, study_selected = filter_select(r_df, "בחרי מחקר", C["study_id"], key="researcher_study_id")

        if not study_df.empty:
            row = study_df.iloc[0]

            show_kpis(
                [
                    ("מספר הלסינקי", str(row.get(C["study_id"], ""))),
                    ("מספר פרוטוקול", str(row.get(C["protocol"], "")) if C["protocol"] else "-"),
                    ("יזם", str(row.get(C["sponsor"], "")) if C["sponsor"] else "-"),
                    ("רמזור", str(row.get("רמזור ניהולי", ""))),
                ]
            )

            display_df(study_df, height=260)

    researcher_excel = download_excel_openpyxl(
        {"גיליון לחוקר": r_df[cols] if cols else r_df}
    )

    st.download_button(
        "⬇️ הורדת גיליון החוקר לאקסל",
        researcher_excel,
        "researcher_report.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


# ============================================================
# 7. Payment tracking
# ============================================================

with tabs[6]:
    st.header("💳 גיליון לחוקר - מעקב דרישות תשלום")

    payment_source = df.copy()

    payment_source, payment_researcher = filter_select(
        payment_source,
        "חוקר",
        C["pi"],
        key="payment_researcher",
    )

    study_ids = (
        payment_source[C["study_id"]].dropna().astype(str).unique().tolist()
        if C["study_id"]
        else []
    )

    protocols = (
        payment_source[C["protocol"]].dropna().astype(str).unique().tolist()
        if C["protocol"]
        else []
    )

    payment_details = details.copy()

    masks = []

    if D["study_id"] and study_ids:
        masks.append(payment_details[D["study_id"]].astype(str).isin(study_ids))

    if D["protocol"] and protocols:
        masks.append(payment_details[D["protocol"]].astype(str).isin(protocols))

    if D["pi_name"] and payment_researcher:
        masks.append(payment_details[D["pi_name"]].astype(str) == str(payment_researcher))

    if masks:
        mask = masks[0]

        for m in masks[1:]:
            mask = mask | m

        payment_details = payment_details[mask]

    if D["study_id"] and not payment_details.empty:
        payment_details = filter_multiselect(payment_details, "מחקר", D["study_id"], key="payment_study")

    show_kpis(
        [
            ("חוקר", payment_researcher or "-"),
            ("סה״כ תקציב", money(sum_col(payment_details, D["budget_total"]))),
            ("התחייבויות רכש", money(sum_col(payment_details, D["purchase_commitments"]))),
            ("סה״כ ביצוע", money(sum_col(payment_details, D["execution_total"]))),
            ("יתרה לניצול", money(sum_col(payment_details, D["balance"]))),
        ]
    )

    if D["budget_category"]:
        cols = [
            D["budget_total"],
            D["purchase_commitments"],
            D["execution_total"],
            D["balance"],
        ]
        cols = [c for c in cols if c]

        if cols:
            summary = (
                payment_details.groupby(D["budget_category"], as_index=False)[cols]
                .sum()
                .rename(columns={D["budget_category"]: "קטגוריית סעיף תקציבי"})
            )

            st.subheader("סיכום לפי קטגוריית סעיף תקציבי")
            display_df(summary, height=280)

            plot_grouped_bar(
                summary,
                "קטגוריית סעיף תקציבי",
                cols,
                "תקציב, התחייבויות, ביצוע ויתרה לפי קטגוריה",
            )

    st.subheader("טבלת מעקב מלאה")
    display_df(payment_details)

    payments_excel = download_excel_openpyxl({"מעקב דרישות תשלום": payment_details})

    st.download_button(
        "⬇️ הורדת מעקב דרישות תשלום לאקסל",
        payments_excel,
        "researcher_payment_tracking.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
