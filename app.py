import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO


# ============================================================
# APP CONFIG
# ============================================================

st.set_page_config(
    page_title="דשבורד מחקרים קליניים",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_VERSION = "v3-professional-dashboard-2026-06-08"


# ============================================================
# CSS DESIGN
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
        padding-top: 1.1rem;
        padding-bottom: 2rem;
        max-width: 1550px;
    }

    section[data-testid="stSidebar"] {
        display: none;
    }

    h1, h2, h3, h4, h5, h6, p, label, span {
        direction: rtl;
        text-align: right;
    }

    .main-hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 52%, #0e7490 100%);
        color: white;
        padding: 28px 32px;
        border-radius: 26px;
        margin-bottom: 22px;
        box-shadow: 0 18px 38px rgba(15, 23, 42, 0.22);
    }

    .main-hero h1 {
        color: white;
        font-size: 2.2rem;
        margin: 0 0 8px 0;
        font-weight: 900;
    }

    .main-hero p {
        color: #dbeafe;
        margin: 0;
        font-size: 1.05rem;
    }

    .section-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 22px;
        padding: 20px 22px;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.055);
    }

    .filter-card {
        background: #f8fafc;
        border: 1px solid #dbe3ef;
        border-radius: 18px;
        padding: 16px 18px;
        margin-bottom: 16px;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #dbe3ef;
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.055);
        min-height: 105px;
    }

    div[data-testid="stMetricLabel"] {
        color: #475569;
        font-size: 0.95rem;
        font-weight: 700;
    }

    div[data-testid="stMetricValue"] {
        color: #0f172a;
        font-size: 1.38rem;
        font-weight: 900;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8fafc;
        border-radius: 18px;
        padding: 8px;
        margin-bottom: 18px;
    }

    .stTabs [data-baseweb="tab"] {
        background: #ffffff;
        border-radius: 14px;
        padding: 11px 18px;
        border: 1px solid #e2e8f0;
        color: #0f172a;
        font-weight: 800;
    }

    .stTabs [aria-selected="true"] {
        background: #dbeafe !important;
        border-color: #60a5fa !important;
        color: #0f172a !important;
    }

    div[data-testid="stDataFrame"] {
        direction: rtl;
        text-align: right;
        border-radius: 18px;
    }

    div[data-testid="stDataFrame"] * {
        direction: rtl;
        text-align: right;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stMultiSelect"] label {
        font-weight: 800;
        color: #1e293b;
    }

    .alert-red {
        background: #fef2f2;
        color: #991b1b;
        border: 1px solid #fecaca;
        border-radius: 16px;
        padding: 14px 16px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .alert-yellow {
        background: #fffbeb;
        color: #92400e;
        border: 1px solid #fde68a;
        border-radius: 16px;
        padding: 14px 16px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .alert-green {
        background: #ecfdf5;
        color: #065f46;
        border: 1px solid #a7f3d0;
        border-radius: 16px;
        padding: 14px 16px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .small-caption {
        color: #64748b;
        font-size: 0.86rem;
        margin-top: -8px;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
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
    for candidate in candidates:
        c = normalize_text(candidate)
        if c in normalized:
            return normalized[c]
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


def compact_number(value):
    try:
        value = float(value)
    except Exception:
        return "0"

    abs_value = abs(value)

    if abs_value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if abs_value >= 1_000:
        return f"{value / 1_000:.0f}K"
    return f"{value:,.0f}"


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


def clean_for_display(df):
    display = df.copy()
    display = display.replace({np.nan: "", None: ""})
    display = display.astype(object)
    return display


def format_table_values(df, money_cols=None, percent_cols=None, number_cols=None, date_cols=None):
    display = clean_for_display(df)

    money_cols = money_cols or []
    percent_cols = percent_cols or []
    number_cols = number_cols or []
    date_cols = date_cols or []

    for col in money_cols:
        if col and col in display.columns:
            display[col] = to_numeric(display[col]).apply(money)

    for col in percent_cols:
        if col and col in display.columns:
            display[col] = to_numeric(display[col]).apply(pct)

    for col in number_cols:
        if col and col in display.columns:
            display[col] = to_numeric(display[col]).apply(number)

    for col in date_cols:
        if col and col in display.columns:
            display[col] = pd.to_datetime(display[col], errors="coerce").dt.strftime("%d/%m/%Y").fillna("")

    return display


def display_table(df, columns=None, title=None, height=420, money_cols=None, percent_cols=None, number_cols=None, date_cols=None):
    if title:
        st.subheader(title)

    if df is None or df.empty:
        st.info("אין נתונים להצגה בהתאם לבחירה הנוכחית.")
        return

    data = df.copy()

    if columns:
        columns = [col for col in columns if col and col in data.columns]
        if columns:
            data = data[columns]

    data = format_table_values(
        data,
        money_cols=money_cols,
        percent_cols=percent_cols,
        number_cols=number_cols,
        date_cols=date_cols,
    )

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True,
        height=height,
    )


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


def shorten_label(value, max_len=24):
    value = str(value)
    if len(value) <= max_len:
        return value
    return value[:max_len - 3] + "..."


def filter_multiselect(df, label, col, key, default_all=True):
    if not col or col not in df.columns:
        return df

    values = sorted(df[col].dropna().astype(str).unique())

    if not values:
        return df.iloc[0:0]

    default = values if default_all else []

    selected = st.multiselect(
        label,
        values,
        default=default,
        key=key,
    )

    if selected:
        return df[df[col].astype(str).isin(selected)]

    return df.iloc[0:0]


def filter_select(df, label, col, key):
    if not col or col not in df.columns:
        return df, None

    values = sorted(df[col].dropna().astype(str).unique())

    if not values:
        return df.iloc[0:0], None

    selected = st.selectbox(label, values, key=key)

    return df[df[col].astype(str) == selected], selected


def show_kpis(items, columns_per_row=5):
    if not items:
        return

    for start in range(0, len(items), columns_per_row):
        chunk = items[start:start + columns_per_row]
        cols = st.columns(len(chunk))
        for col, (label, value) in zip(cols, chunk):
            col.metric(label, value)


def plot_bar(data, x, y, title, x_title=None, y_title=None, height=420):
    if data is None or data.empty or x not in data.columns or y not in data.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    plot_data = data.copy()
    plot_data[x] = plot_data[x].astype(str)
    plot_data["_text"] = plot_data[y].apply(compact_number)

    fig = px.bar(
        plot_data,
        x=x,
        y=y,
        text="_text",
        title=title,
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
    )

    fig.update_layout(
        title_x=0.5,
        height=height,
        bargap=0.35,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=45, r=35, t=80, b=70),
        xaxis=dict(
            type="category",
            tickmode="array",
            tickvals=plot_data[x].tolist(),
            ticktext=plot_data[x].tolist(),
            title=x_title or x,
        ),
        yaxis=dict(
            title=y_title or y,
            gridcolor="#e2e8f0",
        ),
        font=dict(size=13),
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_grouped_bar(data, x, y_cols, title, x_title=None, y_title=None, height=440):
    y_cols = [col for col in y_cols if col and col in data.columns]

    if data is None or data.empty or x not in data.columns or not y_cols:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    plot_data = data.copy()
    plot_data[x] = plot_data[x].astype(str)

    melted = plot_data.melt(
        id_vars=[x],
        value_vars=y_cols,
        var_name="מדד",
        value_name="ערך",
    )

    melted["תווית"] = melted["ערך"].apply(compact_number)

    fig = px.bar(
        melted,
        x=x,
        y="ערך",
        color="מדד",
        barmode="group",
        text="תווית",
        title=title,
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
    )

    fig.update_layout(
        title_x=0.5,
        height=height,
        bargap=0.32,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=45, r=35, t=90, b=70),
        xaxis=dict(
            type="category",
            title=x_title or x,
            tickmode="array",
            tickvals=plot_data[x].astype(str).tolist(),
            ticktext=plot_data[x].astype(str).tolist(),
        ),
        yaxis=dict(
            title=y_title or "סכום",
            gridcolor="#e2e8f0",
        ),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            title="",
        ),
        font=dict(size=13),
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_horizontal_top10(data, label_col, value_col, title, x_title=None, height=None):
    if data is None or data.empty or label_col not in data.columns or value_col not in data.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    plot_data = data.copy()
    plot_data = plot_data.sort_values(value_col, ascending=True).tail(10)

    plot_data["שם מקוצר"] = plot_data[label_col].astype(str).apply(lambda x: shorten_label(x, 32))
    plot_data["שם מלא"] = plot_data[label_col].astype(str)
    plot_data["תווית"] = plot_data[value_col].apply(compact_number)

    if height is None:
        height = max(430, 52 * len(plot_data) + 140)

    fig = px.bar(
        plot_data,
        x=value_col,
        y="שם מקוצר",
        orientation="h",
        text="תווית",
        hover_data={"שם מלא": True, value_col: ":,.0f", "שם מקוצר": False},
        title=title,
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
    )

    fig.update_layout(
        title_x=0.5,
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=230, r=80, t=85, b=55),
        xaxis=dict(
            title=x_title or value_col,
            gridcolor="#e2e8f0",
        ),
        yaxis=dict(
            title="",
            automargin=True,
        ),
        font=dict(size=13),
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_donut(data, names, values, title, height=420):
    if data is None or data.empty or names not in data.columns or values not in data.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    fig = px.pie(
        data,
        names=names,
        values=values,
        hole=0.45,
        title=title,
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
    )

    fig.update_layout(
        title_x=0.5,
        height=height,
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=80, b=20),
        legend=dict(orientation="v", y=0.5),
        font=dict(size=13),
    )

    st.plotly_chart(fig, use_container_width=True)


def find_studies_sheet(xls):
    for sheet_name in xls.sheet_names:
        if normalize_text(sheet_name).lower() == "studies_data":
            return sheet_name
    return xls.sheet_names[0]


def find_details_sheet(xls, studies_sheet):
    for sheet_name in xls.sheet_names:
        if sheet_name == studies_sheet:
            continue

        sample = normalize_columns(pd.read_excel(xls, sheet_name=sheet_name, nrows=10))

        if find_col(sample, ["קטגוריית סעיף תקציבי"]) or find_col(sample, ["מספר הלסינקי"]):
            return sheet_name

    other_sheets = [s for s in xls.sheet_names if s != studies_sheet]

    if other_sheets:
        return other_sheets[0]

    return studies_sheet


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


# ============================================================
# HEADER + FILE UPLOAD
# ============================================================

st.markdown(
    f"""
    <div class="main-hero">
        <h1>📊 דשבורד ניהולי למחקרים קליניים</h1>
        <p>ניתוח מחקרים, הכנסות, הוצאות, תקציבים, חוקרים, מחלקות, יזמים ורמזור ניהולי | {APP_VERSION}</p>
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


# ============================================================
# COLUMN MAPPING
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
# DATA CLEANING + CALCULATIONS
# ============================================================

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

if C["approval_year"] and C["approval_year"] in df.columns:
    df[C["approval_year"]] = df[C["approval_year"]].astype(str).str.replace(".0", "", regex=False)

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
# DISPLAY COLUMN SETS
# ============================================================

study_summary_cols = [
    C["study_id"],
    C["protocol"],
    C["pi"],
    C["department"],
    C["sponsor"],
    C["study_type"],
    C["approval_year"],
    C["expected_income"],
    C["actual_income"],
    C["total_expenses"],
    C["expected_participants"],
    C["actual_participants"],
    "% גיוס משתתפים",
    "% ניצול תקציב - מחושב",
    "סטטוס ניצול תקציב - מחושב",
    "רמזור ניהולי",
]

budget_status_cols = [
    C["study_id"],
    C["protocol"],
    C["pi"],
    C["department"],
    C["sponsor"],
    C["wbs"],
    C["budget_name"],
    C["budget"],
    C["utilization_total"],
    "% ניצול תקציב - מחושב",
    C["balance"],
    C["unreserved_balance"],
    C["end_date"],
    "ימים לסיום",
    "סטטוס גיוס",
    "רמזור ניהולי",
]

researcher_short_cols = [
    C["study_id"],
    C["protocol"],
    C["sponsor"],
    C["wbs"],
    C["budget_name"],
    C["budget"],
    "% ניצול תקציב - מחושב",
    C["balance"],
    "רמזור ניהולי",
]

researcher_identity_cols = [
    C["study_id"],
    C["protocol"],
    C["pi"],
    C["department"],
    C["site"],
    C["sponsor"],
    C["study_type"],
    C["phase"],
    C["start_date"],
    C["end_date"],
    C["budget_name"],
    C["budget_owner"],
    C["wbs"],
    C["contract"],
    C["budget"],
    C["execution"],
    C["commitment"],
    C["utilization_total"],
    C["balance"],
    C["unreserved_balance"],
    "% ניצול תקציב - מחושב",
    C["expected_participants"],
    C["actual_participants"],
    "% גיוס משתתפים",
    "סטטוס גיוס",
    "רמזור ניהולי",
]

payment_cols = [
    D["wbs"],
    D["study_id"],
    D["protocol"],
    D["pi_name"],
    D["site"],
    D["budget_category"],
    D["commitment_group"],
    D["commitment_group_desc"],
    D["description"],
    D["budget_total"],
    D["purchase_commitments"],
    D["execution_total"],
    D["balance"],
]

money_table_cols = [
    C["expected_income"],
    C["actual_income"],
    C["total_expenses"],
    C["budget"],
    C["execution"],
    C["commitment"],
    C["utilization_total"],
    C["balance"],
    C["unreserved_balance"],
    D["budget_total"],
    D["purchase_commitments"],
    D["execution_total"],
    D["balance"],
]

percent_table_cols = [
    "% ניצול תקציב - מחושב",
    "% גיוס משתתפים",
]

number_table_cols = [
    C["expected_participants"],
    C["actual_participants"],
    "ימים לסיום",
]

date_table_cols = [
    C["approval_date"],
    C["start_date"],
    C["end_date"],
]


# ============================================================
# TABS
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
# TAB 1 - HOSPITAL
# ============================================================

with tabs[0]:
    st.header("🏥 כלל בית החולים")

    hospital = df.copy()

    f1, f2, f3 = st.columns(3)

    with f1:
        hospital = filter_multiselect(hospital, "שנה", C["approval_year"], key="hospital_year")

    with f2:
        hospital = filter_multiselect(hospital, "סוג מימון", C["funding_type"], key="hospital_funding")

    with f3:
        hospital = filter_multiselect(hospital, "סוג מחקר", C["study_type"], key="hospital_type")

    show_kpis(
        [
            ("סה״כ מחקרים", number(count_unique_studies(hospital, C["unique_study"], C["study_id"]))),
            ("מספר חוקרים", number(hospital[C["pi"]].nunique() if C["pi"] else 0)),
            ("צפי הכנסות", money(sum_col(hospital, C["expected_income"]))),
            ("הכנסות בפועל", money(sum_col(hospital, C["actual_income"]))),
            ("סך הוצאות", money(sum_col(hospital, C["total_expenses"]))),
        ],
        columns_per_row=5,
    )

    st.markdown("")

    if C["approval_year"]:
        yearly_count = (
            hospital.groupby(C["approval_year"], as_index=False)[C["unique_study"]]
            .sum()
            .rename(columns={C["approval_year"]: "שנה", C["unique_study"]: "מספר מחקרים"})
            if C["unique_study"]
            else hospital.groupby(C["approval_year"], as_index=False)
            .size()
            .rename(columns={C["approval_year"]: "שנה", "size": "מספר מחקרים"})
        )

        yearly_count["שנה"] = yearly_count["שנה"].astype(str)

        plot_bar(
            yearly_count,
            "שנה",
            "מספר מחקרים",
            "סה״כ מחקרים לפי שנה",
            x_title="שנה",
            y_title="מספר מחקרים",
            height=390,
        )

        money_cols_year = [
            C["expected_income"],
            C["actual_income"],
            C["total_expenses"],
            C["overhead"],
        ]
        money_cols_year = [c for c in money_cols_year if c]

        if money_cols_year:
            yearly_money = (
                hospital.groupby(C["approval_year"], as_index=False)[money_cols_year]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )
            yearly_money["שנה"] = yearly_money["שנה"].astype(str)

            plot_grouped_bar(
                yearly_money,
                "שנה",
                money_cols_year,
                "צפי הכנסות, הכנסות בפועל, הוצאות ותקורה לפי שנה",
                x_title="שנה",
                y_title="סכום",
                height=430,
            )

    c1, c2 = st.columns(2)

    with c1:
        if C["funding_type"] and C["unique_study"]:
            funding = (
                hospital.groupby(C["funding_type"], as_index=False)[C["unique_study"]]
                .sum()
                .rename(columns={C["funding_type"]: "סוג מימון", C["unique_study"]: "מספר מחקרים"})
            )

            plot_donut(
                funding,
                "סוג מימון",
                "מספר מחקרים",
                "התפלגות מחקרים לפי סוג מימון",
                height=390,
            )

    with c2:
        if C["pi"] and C["unique_study"]:
            researcher_counts = (
                hospital.groupby(C["pi"], as_index=False)[C["unique_study"]]
                .sum()
                .rename(columns={C["unique_study"]: "מספר מחקרים"})
            )

            researcher_counts["טווח מחקרים לחוקר"] = pd.cut(
                researcher_counts["מספר מחקרים"],
                bins=[0, 5, 10, 20, 50, np.inf],
                labels=["1-5", "6-10", "11-20", "21-50", "50+"],
                include_lowest=True,
            )

            dist = (
                researcher_counts.groupby("טווח מחקרים לחוקר", as_index=False, observed=False)
                .size()
                .rename(columns={"size": "מספר חוקרים"})
            )

            plot_donut(
                dist,
                "טווח מחקרים לחוקר",
                "מספר חוקרים",
                "התפלגות כמות מחקרים לחוקר",
                height=390,
            )

    c3, c4 = st.columns(2)

    with c3:
        if C["pi"] and C["unique_study"]:
            top_pi_count = (
                hospital.groupby(C["pi"], as_index=False)[C["unique_study"]]
                .sum()
                .sort_values(C["unique_study"], ascending=False)
                .head(10)
                .rename(columns={C["pi"]: "חוקר ראשי", C["unique_study"]: "מספר מחקרים"})
            )

            plot_horizontal_top10(
                top_pi_count,
                "חוקר ראשי",
                "מספר מחקרים",
                "Top 10 חוקרים לפי כמות מחקרים",
                x_title="מספר מחקרים",
            )

    with c4:
        if C["pi"] and C["expected_income"]:
            top_pi_income = (
                hospital.groupby(C["pi"], as_index=False)[C["expected_income"]]
                .sum()
                .sort_values(C["expected_income"], ascending=False)
                .head(10)
                .rename(columns={C["pi"]: "חוקר ראשי", C["expected_income"]: "צפי הכנסות"})
            )

            plot_horizontal_top10(
                top_pi_income,
                "חוקר ראשי",
                "צפי הכנסות",
                "Top 10 חוקרים לפי צפי הכנסות",
                x_title="צפי הכנסות",
            )


# ============================================================
# TAB 2 - DEPARTMENTS
# ============================================================

with tabs[1]:
    st.header("🏢 מחלקות")

    dept = df.copy()

    f1, f2 = st.columns(2)

    with f1:
        dept, selected_dept = filter_select(dept, "מחלקה", C["department"], key="dept_select")

    with f2:
        dept = filter_multiselect(dept, "שנה", C["approval_year"], key="dept_year")

    show_kpis(
        [
            ("מחלקה", selected_dept or "-"),
            ("מספר מחקרים", number(count_unique_studies(dept, C["unique_study"], C["study_id"]))),
            ("צפי הכנסות", money(sum_col(dept, C["expected_income"]))),
            ("הכנסות בפועל", money(sum_col(dept, C["actual_income"]))),
            ("סך הוצאות", money(sum_col(dept, C["total_expenses"]))),
        ],
        columns_per_row=5,
    )

    if C["approval_year"]:
        dept_money_cols = [
            C["expected_income"],
            C["actual_income"],
            C["total_expenses"],
        ]
        dept_money_cols = [c for c in dept_money_cols if c]

        if dept_money_cols:
            dept_year = (
                dept.groupby(C["approval_year"], as_index=False)[dept_money_cols]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )
            dept_year["שנה"] = dept_year["שנה"].astype(str)

            plot_grouped_bar(
                dept_year,
                "שנה",
                dept_money_cols,
                "הכנסות והוצאות לפי שנה במחלקה",
                x_title="שנה",
                y_title="סכום",
                height=420,
            )

        if C["expected_participants"] and C["actual_participants"]:
            participants = (
                dept.groupby(C["approval_year"], as_index=False)[
                    [C["expected_participants"], C["actual_participants"]]
                ]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )
            participants["שנה"] = participants["שנה"].astype(str)

            plot_grouped_bar(
                participants,
                "שנה",
                [C["expected_participants"], C["actual_participants"]],
                "צפי משתתפים מול משתתפים בפועל",
                x_title="שנה",
                y_title="מספר משתתפים",
                height=390,
            )

    display_table(
        dept,
        columns=study_summary_cols,
        title="טבלת מחקרים במחלקה",
        height=430,
        money_cols=money_table_cols,
        percent_cols=percent_table_cols,
        number_cols=number_table_cols,
        date_cols=date_table_cols,
    )


# ============================================================
# TAB 3 - RESEARCHERS
# ============================================================

with tabs[2]:
    st.header("👩‍⚕️ חוקרים")

    pi_df = df.copy()

    f1, f2 = st.columns(2)

    with f1:
        pi_df, selected_pi = filter_select(pi_df, "חוקר ראשי", C["pi"], key="pi_select")

    with f2:
        pi_df = filter_multiselect(pi_df, "שנה", C["approval_year"], key="pi_year")

    show_kpis(
        [
            ("חוקר", selected_pi or "-"),
            ("מספר מחקרים", number(count_unique_studies(pi_df, C["unique_study"], C["study_id"]))),
            ("צפי הכנסות", money(sum_col(pi_df, C["expected_income"]))),
            ("הכנסות בפועל", money(sum_col(pi_df, C["actual_income"]))),
            ("סך הוצאות", money(sum_col(pi_df, C["total_expenses"]))),
        ],
        columns_per_row=5,
    )

    if C["approval_year"]:
        pi_money_cols = [
            C["expected_income"],
            C["actual_income"],
            C["total_expenses"],
        ]
        pi_money_cols = [c for c in pi_money_cols if c]

        if pi_money_cols:
            pi_year = (
                pi_df.groupby(C["approval_year"], as_index=False)[pi_money_cols]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )
            pi_year["שנה"] = pi_year["שנה"].astype(str)

            plot_grouped_bar(
                pi_year,
                "שנה",
                pi_money_cols,
                "הכנסות מול הוצאות לפי שנה לחוקר",
                x_title="שנה",
                y_title="סכום",
                height=420,
            )

        expense_cols = [
            C["salary_expenses"],
            C["materials_expenses"],
            C["fixed_expenses"],
            C["travel_expenses"],
            C["internal_expenses"],
        ]
        expense_cols = [c for c in expense_cols if c]

        if expense_cols:
            pi_exp = (
                pi_df.groupby(C["approval_year"], as_index=False)[expense_cols]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )
            pi_exp["שנה"] = pi_exp["שנה"].astype(str)

            plot_grouped_bar(
                pi_exp,
                "שנה",
                expense_cols,
                "התפלגות הוצאות לפי שנה לחוקר",
                x_title="שנה",
                y_title="סכום",
                height=420,
            )

        if C["expected_participants"] and C["actual_participants"]:
            pi_participants = (
                pi_df.groupby(C["approval_year"], as_index=False)[
                    [C["expected_participants"], C["actual_participants"]]
                ]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )
            pi_participants["שנה"] = pi_participants["שנה"].astype(str)

            plot_grouped_bar(
                pi_participants,
                "שנה",
                [C["expected_participants"], C["actual_participants"]],
                "צפי משתתפים מול משתתפים בפועל לחוקר",
                x_title="שנה",
                y_title="מספר משתתפים",
                height=390,
            )

    display_table(
        pi_df,
        columns=study_summary_cols,
        title="טבלת מחקרים לחוקר",
        height=430,
        money_cols=money_table_cols,
        percent_cols=percent_table_cols,
        number_cols=number_table_cols,
        date_cols=date_table_cols,
    )


# ============================================================
# TAB 4 - SPONSORS
# ============================================================

with tabs[3]:
    st.header("🏭 יזמים")

    sponsor_df = df.copy()

    f1, f2 = st.columns(2)

    with f1:
        sponsor_df = filter_multiselect(sponsor_df, "יזם", C["sponsor"], key="sponsor_select")

    with f2:
        sponsor_df = filter_multiselect(sponsor_df, "שנה", C["approval_year"], key="sponsor_year")

    if C["sponsor"]:
        sponsor_summary = sponsor_df.groupby(C["sponsor"], as_index=False).agg(
            מספר_רשומות=(C["sponsor"], "size")
        )

        if C["unique_study"]:
            study_count = (
                sponsor_df.groupby(C["sponsor"], as_index=False)[C["unique_study"]]
                .sum()
                .rename(columns={C["unique_study"]: "מספר מחקרים"})
            )
            sponsor_summary = sponsor_summary.merge(study_count, on=C["sponsor"], how="left")
        else:
            sponsor_summary["מספר מחקרים"] = sponsor_summary["מספר_רשומות"]

        if C["expected_income"]:
            income_summary = (
                sponsor_df.groupby(C["sponsor"], as_index=False)[C["expected_income"]]
                .sum()
                .rename(columns={C["expected_income"]: "צפי הכנסות"})
            )
            sponsor_summary = sponsor_summary.merge(income_summary, on=C["sponsor"], how="left")

        if C["actual_income"]:
            actual_summary = (
                sponsor_df.groupby(C["sponsor"], as_index=False)[C["actual_income"]]
                .sum()
                .rename(columns={C["actual_income"]: "הכנסות בפועל"})
            )
            sponsor_summary = sponsor_summary.merge(actual_summary, on=C["sponsor"], how="left")

        if C["total_expenses"]:
            expense_summary = (
                sponsor_df.groupby(C["sponsor"], as_index=False)[C["total_expenses"]]
                .sum()
                .rename(columns={C["total_expenses"]: "סך הוצאות"})
            )
            sponsor_summary = sponsor_summary.merge(expense_summary, on=C["sponsor"], how="left")

        if C["pi"]:
            pi_summary = (
                sponsor_df.groupby(C["sponsor"], as_index=False)[C["pi"]]
                .nunique()
                .rename(columns={C["pi"]: "מספר חוקרים"})
            )
            sponsor_summary = sponsor_summary.merge(pi_summary, on=C["sponsor"], how="left")

        if C["department"]:
            dept_summary = (
                sponsor_df.groupby(C["sponsor"], as_index=False)[C["department"]]
                .nunique()
                .rename(columns={C["department"]: "מספר מחלקות"})
            )
            sponsor_summary = sponsor_summary.merge(dept_summary, on=C["sponsor"], how="left")

        sponsor_summary = sponsor_summary.rename(columns={C["sponsor"]: "יזם"})

        c1, c2 = st.columns(2)

        with c1:
            if "מספר מחקרים" in sponsor_summary.columns:
                count_data = sponsor_summary[["יזם", "מספר מחקרים"]].sort_values("מספר מחקרים", ascending=False)
                top_count = count_data.head(10)
                other_count = count_data.iloc[10:]["מספר מחקרים"].sum()

                if other_count > 0:
                    top_count = pd.concat(
                        [top_count, pd.DataFrame({"יזם": ["אחר"], "מספר מחקרים": [other_count]})],
                        ignore_index=True,
                    )

                plot_donut(
                    top_count,
                    "יזם",
                    "מספר מחקרים",
                    "התפלגות כמות מחקרים לפי יזם - Top 10 ואחר",
                    height=410,
                )

        with c2:
            if "צפי הכנסות" in sponsor_summary.columns:
                income_data = sponsor_summary[["יזם", "צפי הכנסות"]].sort_values("צפי הכנסות", ascending=False)
                top_income = income_data.head(10)
                other_income = income_data.iloc[10:]["צפי הכנסות"].sum()

                if other_income > 0:
                    top_income = pd.concat(
                        [top_income, pd.DataFrame({"יזם": ["אחר"], "צפי הכנסות": [other_income]})],
                        ignore_index=True,
                    )

                plot_donut(
                    top_income,
                    "יזם",
                    "צפי הכנסות",
                    "התפלגות צפי הכנסות לפי יזם - Top 10 ואחר",
                    height=410,
                )

        c3, c4 = st.columns(2)

        with c3:
            if "מספר מחקרים" in sponsor_summary.columns:
                plot_horizontal_top10(
                    sponsor_summary.sort_values("מספר מחקרים", ascending=False).head(10),
                    "יזם",
                    "מספר מחקרים",
                    "Top 10 יזמים לפי כמות מחקרים",
                    x_title="מספר מחקרים",
                )

        with c4:
            if "צפי הכנסות" in sponsor_summary.columns:
                plot_horizontal_top10(
                    sponsor_summary.sort_values("צפי הכנסות", ascending=False).head(10),
                    "יזם",
                    "צפי הכנסות",
                    "Top 10 יזמים לפי צפי הכנסות",
                    x_title="צפי הכנסות",
                )

        display_table(
            sponsor_summary.sort_values("מספר מחקרים", ascending=False) if "מספר מחקרים" in sponsor_summary.columns else sponsor_summary,
            title="טבלת סיכום יזמים",
            height=430,
            money_cols=["צפי הכנסות", "הכנסות בפועל", "סך הוצאות"],
            number_cols=["מספר מחקרים", "מספר חוקרים", "מספר מחלקות"],
        )


# ============================================================
# TAB 5 - BUDGET STATUS
# ============================================================

with tabs[4]:
    st.header("🚦 סטטוס ניהול תקציב")

    status_df = df.copy()

    f1, f2, f3 = st.columns(3)

    with f1:
        status_df = filter_multiselect(status_df, "שנה", C["approval_year"], key="status_year")

    with f2:
        status_df = filter_multiselect(status_df, "מחלקה", C["department"], key="status_dept")

    with f3:
        status_df = filter_multiselect(status_df, "חוקר ראשי", C["pi"], key="status_pi")

    f4, f5, f6 = st.columns(3)

    with f4:
        status_df = filter_multiselect(status_df, "סטטוס ניצול", "סטטוס ניצול תקציב - מחושב", key="status_util")

    with f5:
        status_df = filter_multiselect(status_df, "רמזור", "רמזור ניהולי", key="status_light")

    with f6:
        status_df = filter_multiselect(status_df, "סטטוס גיוס", "סטטוס גיוס", key="status_recruit")

    over_budget = status_df[status_df["סטטוס ניצול תקציב - מחושב"] == "חריגה"]
    high_util = status_df[status_df["סטטוס ניצול תקציב - מחושב"] == "קרוב לניצול מלא"]
    low_util = status_df[status_df["סטטוס ניצול תקציב - מחושב"] == "ניצול נמוך"]
    low_recruit = status_df[status_df["סטטוס גיוס"].isin(["אין גיוס", "גיוס נמוך"])]
    ending_soon = status_df[(status_df["ימים לסיום"] >= 0) & (status_df["ימים לסיום"] <= 60)]

    show_kpis(
        [
            ("🔴 מחקרים בחריגה", number(len(over_budget))),
            ("🟡 קרוב לניצול מלא", number(len(high_util))),
            ("🟡 ניצול נמוך", number(len(low_util))),
            ("🟡 גיוס נמוך / אין גיוס", number(len(low_recruit))),
            ("🟡 מסתיימים תוך 60 יום", number(len(ending_soon))),
        ],
        columns_per_row=5,
    )

    c1, c2 = st.columns(2)

    with c1:
        status_summary = (
            status_df.groupby("סטטוס ניצול תקציב - מחושב", as_index=False)
            .size()
            .rename(columns={"size": "מספר מחקרים"})
        )

        plot_donut(
            status_summary,
            "סטטוס ניצול תקציב - מחושב",
            "מספר מחקרים",
            "התפלגות סטטוס ניצול תקציבי",
            height=390,
        )

    with c2:
        recruit_summary = (
            status_df.groupby("סטטוס גיוס", as_index=False)
            .size()
            .rename(columns={"size": "מספר מחקרים"})
        )

        plot_donut(
            recruit_summary,
            "סטטוס גיוס",
            "מספר מחקרים",
            "התפלגות סטטוס גיוס משתתפים",
            height=390,
        )

    alert_tabs = st.tabs(
        [
            "🔴 חריגה תקציבית",
            "🟡 קרוב לניצול מלא",
            "🟡 ניצול נמוך",
            "🟡 גיוס נמוך",
            "🟡 סיום קרוב",
            "📋 כל הסטטוסים",
        ]
    )

    with alert_tabs[0]:
        display_table(
            over_budget,
            columns=budget_status_cols,
            title="מחקרים בחריגה תקציבית",
            height=390,
            money_cols=money_table_cols,
            percent_cols=percent_table_cols,
            number_cols=number_table_cols,
            date_cols=date_table_cols,
        )

    with alert_tabs[1]:
        display_table(
            high_util,
            columns=budget_status_cols,
            title="מחקרים קרובים לניצול מלא",
            height=390,
            money_cols=money_table_cols,
            percent_cols=percent_table_cols,
            number_cols=number_table_cols,
            date_cols=date_table_cols,
        )

    with alert_tabs[2]:
        display_table(
            low_util,
            columns=budget_status_cols,
            title="מחקרים בניצול נמוך",
            height=390,
            money_cols=money_table_cols,
            percent_cols=percent_table_cols,
            number_cols=number_table_cols,
            date_cols=date_table_cols,
        )

    with alert_tabs[3]:
        display_table(
            low_recruit,
            columns=budget_status_cols,
            title="מחקרים עם גיוס משתתפים נמוך / ללא גיוס",
            height=390,
            money_cols=money_table_cols,
            percent_cols=percent_table_cols,
            number_cols=number_table_cols,
            date_cols=date_table_cols,
        )

    with alert_tabs[4]:
        display_table(
            ending_soon,
            columns=budget_status_cols,
            title="מחקרים שמסתיימים תוך 60 יום",
            height=390,
            money_cols=money_table_cols,
            percent_cols=percent_table_cols,
            number_cols=number_table_cols,
            date_cols=date_table_cols,
        )

    with alert_tabs[5]:
        display_table(
            status_df,
            columns=budget_status_cols,
            title="טבלת סטטוס ניהול תקציב",
            height=430,
            money_cols=money_table_cols,
            percent_cols=percent_table_cols,
            number_cols=number_table_cols,
            date_cols=date_table_cols,
        )


# ============================================================
# TAB 6 - RESEARCHER SHEET
# ============================================================

with tabs[5]:
    st.header("🧾 גיליון לחוקר")

    r_df = df.copy()

    f1, f2 = st.columns(2)

    with f1:
        r_df, selected_researcher = filter_select(r_df, "חוקר", C["pi"], key="researcher_sheet_select")

    with f2:
        r_df = filter_multiselect(r_df, "שנה", C["approval_year"], key="researcher_sheet_year")

    show_kpis(
        [
            ("חוקר", selected_researcher or "-"),
            ("מספר מחקרים", number(count_unique_studies(r_df, C["unique_study"], C["study_id"]))),
            ("תקציב כולל", money(sum_col(r_df, C["budget"]))),
            ("סה״כ ניצול", money(sum_col(r_df, C["utilization_total"]))),
            ("יתרה לניצול", money(sum_col(r_df, C["balance"]))),
        ],
        columns_per_row=5,
    )

    display_table(
        r_df,
        columns=researcher_short_cols,
        title="רשימת מחקרים מקוצרת לחוקר",
        height=320,
        money_cols=money_table_cols,
        percent_cols=percent_table_cols,
        number_cols=number_table_cols,
        date_cols=date_table_cols,
    )

    if C["study_id"] and not r_df.empty:
        st.subheader("תעודת זהות למחקר")

        selected_study_df, selected_study = filter_select(
            r_df,
            "בחרי מחקר לפתיחת תעודת זהות",
            C["study_id"],
            key="researcher_identity_study",
        )

        if not selected_study_df.empty:
            row = selected_study_df.iloc[0]

            show_kpis(
                [
                    ("מספר הלסינקי", str(row.get(C["study_id"], ""))),
                    ("מספר פרוטוקול", str(row.get(C["protocol"], "")) if C["protocol"] else "-"),
                    ("יזם", str(row.get(C["sponsor"], "")) if C["sponsor"] else "-"),
                    ("רמזור", str(row.get("רמזור ניהולי", ""))),
                    ("% ניצול", pct(row.get("% ניצול תקציב - מחושב", 0))),
                ],
                columns_per_row=5,
            )

            display_table(
                selected_study_df,
                columns=researcher_identity_cols,
                title="פרטי המחקר שנבחר",
                height=360,
                money_cols=money_table_cols,
                percent_cols=percent_table_cols,
                number_cols=number_table_cols,
                date_cols=date_table_cols,
            )

    researcher_excel = download_excel_openpyxl(
        {
            "researcher_short": r_df[[c for c in researcher_short_cols if c and c in r_df.columns]],
            "researcher_full": r_df,
        }
    )

    st.download_button(
        "⬇️ הורדת גיליון החוקר לאקסל",
        researcher_excel,
        "researcher_report.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


# ============================================================
# TAB 7 - PAYMENT TRACKING
# ============================================================

with tabs[6]:
    st.header("💳 גיליון לחוקר - מעקב דרישות תשלום")

    payment_source = df.copy()

    payment_source, payment_researcher = filter_select(
        payment_source,
        "חוקר",
        C["pi"],
        key="payment_researcher_select",
    )

    study_ids = (
        payment_source[C["study_id"]].dropna().astype(str).unique().tolist()
        if C["study_id"] and C["study_id"] in payment_source.columns
        else []
    )

    protocols = (
        payment_source[C["protocol"]].dropna().astype(str).unique().tolist()
        if C["protocol"] and C["protocol"] in payment_source.columns
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
        combined = masks[0]
        for mask in masks[1:]:
            combined = combined | mask
        payment_details = payment_details[combined]

    if D["study_id"] and not payment_details.empty:
        payment_details = filter_multiselect(
            payment_details,
            "מחקר",
            D["study_id"],
            key="payment_study_filter",
        )

    show_kpis(
        [
            ("חוקר", payment_researcher or "-"),
            ("סה״כ תקציב", money(sum_col(payment_details, D["budget_total"]))),
            ("התחייבויות רכש", money(sum_col(payment_details, D["purchase_commitments"]))),
            ("סה״כ ביצוע", money(sum_col(payment_details, D["execution_total"]))),
            ("יתרה לניצול", money(sum_col(payment_details, D["balance"]))),
        ],
        columns_per_row=5,
    )

    if D["budget_category"]:
        summary_cols = [
            D["budget_total"],
            D["purchase_commitments"],
            D["execution_total"],
            D["balance"],
        ]
        summary_cols = [c for c in summary_cols if c]

        if summary_cols:
            category_summary = (
                payment_details.groupby(D["budget_category"], as_index=False)[summary_cols]
                .sum()
                .rename(columns={D["budget_category"]: "קטגוריית סעיף תקציבי"})
            )

            c1, c2 = st.columns([1, 1])

            with c1:
                display_table(
                    category_summary,
                    title="סיכום לפי קטגוריית סעיף תקציבי",
                    height=320,
                    money_cols=summary_cols,
                )

            with c2:
                plot_grouped_bar(
                    category_summary,
                    "קטגוריית סעיף תקציבי",
                    summary_cols,
                    "תקציב, התחייבויות, ביצוע ויתרה לפי קטגוריה",
                    x_title="קטגוריה",
                    y_title="סכום",
                    height=360,
                )

    if D["wbs"] and D["budget_total"]:
        wbs_summary_cols = [
            D["budget_total"],
            D["purchase_commitments"],
            D["execution_total"],
            D["balance"],
        ]
        wbs_summary_cols = [c for c in wbs_summary_cols if c]

        if wbs_summary_cols:
            wbs_summary = (
                payment_details.groupby(D["wbs"], as_index=False)[wbs_summary_cols]
                .sum()
                .rename(columns={D["wbs"]: "אלמנט WBS"})
            )

            display_table(
                wbs_summary,
                title="סיכום לפי WBS",
                height=280,
                money_cols=wbs_summary_cols,
            )

    display_table(
        payment_details,
        columns=payment_cols,
        title="טבלת מעקב דרישות תשלום",
        height=430,
        money_cols=money_table_cols,
        percent_cols=percent_table_cols,
        number_cols=number_table_cols,
        date_cols=date_table_cols,
    )

    payments_excel = download_excel_openpyxl(
        {
            "payment_tracking": payment_details,
        }
    )

    st.download_button(
        "⬇️ הורדת מעקב דרישות תשלום לאקסל",
        payments_excel,
        "researcher_payment_tracking.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
