import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
from html import escape


# ============================================================
# APP CONFIG
# ============================================================

st.set_page_config(
    page_title="דשבורד מחקרים קליניים",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_VERSION = "v7-financial-insights-no-risk-2026-06-09"


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    div[data-testid="stFileUploader"] {
    background: #ffffff;
    border: 1px solid #dbe3ef;
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 18px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 20px !important;
    border-color: #dbe3ef !important;
    background: #ffffff !important;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
}

div[data-testid="stSelectbox"],
div[data-testid="stMultiSelect"] {
    direction: rtl;
    text-align: right;
}

div[data-baseweb="select"] {
    direction: rtl;
    text-align: right;
}

.page-header {
    border-right: 7px solid #2563eb;
}
    
    <style>
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: Arial, sans-serif;
        background-color: #f3f6fb;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }

    h1, h2, h3, h4, h5, h6, p, label, span {
        direction: rtl;
        text-align: right;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        color: white;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
        background: rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 6px 8px;
        margin-bottom: 4px;
    }

    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 48%, #0f766e 100%);
        color: white;
        padding: 30px 36px;
        border-radius: 28px;
        margin-bottom: 22px;
        box-shadow: 0 18px 42px rgba(15, 23, 42, 0.22);
    }

    .hero h1 {
        color: white;
        font-size: 2.2rem;
        margin: 0 0 8px 0;
        font-weight: 900;
        letter-spacing: -0.5px;
    }

    .hero p {
        color: #dbeafe;
        margin: 0;
        font-size: 1.02rem;
    }

    .page-header {
        background: #ffffff;
        border: 1px solid #dbe3ef;
        border-radius: 24px;
        padding: 20px 24px;
        margin-bottom: 18px;
        box-shadow: 0 10px 26px rgba(15, 23, 42, 0.055);
    }

    .page-header h2 {
        color: #0f172a;
        font-size: 1.55rem;
        font-weight: 950;
        margin: 0 0 6px 0;
    }

    .page-header p {
        color: #64748b;
        font-size: 0.95rem;
        margin: 0;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #dbe3ef;
        padding: 18px;
        border-radius: 20px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.055);
        min-height: 110px;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 800;
    }

    div[data-testid="stMetricValue"] {
        color: #0f172a;
        font-size: 1.35rem;
        font-weight: 950;
    }

    div[data-testid="stMetricDelta"] {
        direction: ltr;
        text-align: right;
    }

    .insight-box {
    background: #ffffff;
    border: 1px solid #dbe3ef;
    border-radius: 22px;
    padding: 18px 20px;
    margin-bottom: 18px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
    direction: rtl;
    text-align: right;
}

.insight-title {
    color: #0f172a;
    font-size: 1.12rem;
    font-weight: 950;
    margin-bottom: 10px;
    direction: rtl;
    text-align: right;
}

.insight-item {
    background: #f8fafc;
    border-right: 5px solid #2563eb;
    border-left: none;
    border-radius: 14px;
    padding: 10px 12px;
    margin-bottom: 8px;
    color: #0f172a;
    font-weight: 700;
    direction: rtl;
    text-align: right;
    unicode-bidi: plaintext;
}

    .insight-warning {
        border-right-color: #f59e0b;
        background: #fffbeb;
    }

    .insight-danger {
        border-right-color: #ef4444;
        background: #fef2f2;
    }

    .insight-success {
        border-right-color: #10b981;
        background: #ecfdf5;
    }

    .chart-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 22px;
        padding: 16px 18px 8px 18px;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
    }

    .table-wrap {
        background: #ffffff;
        border: 1px solid #dbe3ef;
        border-radius: 22px;
        padding: 14px;
        margin-top: 8px;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
    }

    .table-title {
        color: #0f172a;
        font-size: 1.18rem;
        font-weight: 950;
        margin-bottom: 10px;
    }

    .table-scroll {
        overflow: auto;
        max-height: 430px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
    }

    table.prof-table {
        width: 100%;
        border-collapse: collapse;
        direction: rtl;
        text-align: right;
        font-size: 0.9rem;
        background: white;
    }

    table.prof-table thead th {
        position: sticky;
        top: 0;
        z-index: 2;
        background: #0f172a;
        color: white;
        padding: 11px 12px;
        border-bottom: 1px solid #334155;
        white-space: nowrap;
        font-weight: 900;
    }

    table.prof-table tbody td {
        padding: 10px 12px;
        border-bottom: 1px solid #e5e7eb;
        color: #0f172a;
        white-space: nowrap;
        max-width: 280px;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    table.prof-table tbody tr:nth-child(even) {
        background: #f8fafc;
    }

    table.prof-table tbody tr:hover {
        background: #e0f2fe;
    }

    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        font-weight: 900;
        font-size: 0.78rem;
        white-space: nowrap;
    }

    .badge-red {
        background: #fee2e2;
        color: #991b1b;
        border: 1px solid #fecaca;
    }

    .badge-yellow {
        background: #fef3c7;
        color: #92400e;
        border: 1px solid #fde68a;
    }

    .badge-green {
        background: #dcfce7;
        color: #166534;
        border: 1px solid #bbf7d0;
    }

    .badge-blue {
        background: #dbeafe;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
    }

    .identity-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(190px, 1fr));
        gap: 14px;
        margin: 10px 0 20px 0;
    }

    .identity-card {
        background: #ffffff;
        border: 1px solid #dbe3ef;
        border-radius: 18px;
        padding: 14px 16px;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.045);
        min-height: 88px;
    }

    .identity-label {
        color: #64748b;
        font-size: 0.82rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .identity-value {
        color: #0f172a;
        font-size: 1.02rem;
        font-weight: 900;
        word-break: break-word;
    }

    .explain-box {
        background: #ffffff;
        border: 1px solid #dbe3ef;
        border-radius: 18px;
        padding: 14px 16px;
        margin-bottom: 14px;
    }

    @media (max-width: 1000px) {
        .identity-grid {
            grid-template-columns: repeat(2, 1fr);
        }
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
    return " ".join(value.split()).strip()


def normalize_columns(df):
    df = df.copy()
    df.columns = [normalize_text(col) for col in df.columns]
    return df


def find_col(df, candidates):
    normalized = {normalize_text(col): col for col in df.columns}
    for candidate in candidates:
        candidate = normalize_text(candidate)
        if candidate in normalized:
            return normalized[candidate]
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
        val = to_numeric(df[unique_col]).sum()
        if val > 0:
            return val

    if study_id_col and study_id_col in df.columns:
        return df[study_id_col].dropna().astype(str).nunique()

    return len(df)


def safe_value(value):
    if pd.isna(value):
        return ""
    if value is None:
        return ""
    text = str(value)
    if text.lower() in ["nan", "none", "nat"]:
        return ""
    if text.endswith(".0") and text.replace(".0", "").replace("-", "").isdigit():
        text = text.replace(".0", "")
    return text


def download_excel_openpyxl(sheets_dict):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, data in sheets_dict.items():
            safe_name = str(sheet_name)[:31]
            if data is None:
                data = pd.DataFrame()
            data.to_excel(writer, index=False, sheet_name=safe_name)
    return output.getvalue()


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

def classify_funding_group(value):
    text = normalize_text(value).lower()

    if any(word in text for word in ["גרנט", "grant", "מענק"]):
        return "גרנט"

    if any(word in text for word in ["יזם", "industry", "commercial", "חברה"]):
        return "מחקר יזם"

    if text.strip() == "":
        return "לא סווג"

    return "אחר"


def add_revenue_realization(df, expected_col, actual_col):
    data = df.copy()

    if expected_col and actual_col and expected_col in data.columns and actual_col in data.columns:
        expected = to_numeric(data[expected_col])
        actual = to_numeric(data[actual_col])
        data["שיעור מימוש הכנסות"] = np.where(expected > 0, actual / expected * 100, 0)
    else:
        data["שיעור מימוש הכנסות"] = 0

    return data


def build_clean_insights(data, funding_group_col=None):
    insights = []

    total_studies = count_unique_studies(data, C["unique_study"], C["study_id"])
    expected_income = sum_col(data, C["expected_income"])
    actual_income = sum_col(data, C["actual_income"])
    total_expenses = sum_col(data, C["total_expenses"])

    insights.append((f"סה״כ מוצגים {number(total_studies)} מחקרים בהתאם לסינון הנוכחי.", "success"))

    if expected_income > 0:
        realization = actual_income / expected_income * 100
        if realization >= 80:
            kind = "success"
        elif realization >= 50:
            kind = "warning"
        else:
            kind = "danger"

        insights.append((f"שיעור מימוש ההכנסות בפועל מתוך צפי ההכנסות הוא {pct(realization)}.", kind))

    if actual_income > 0:
        expense_ratio = total_expenses / actual_income * 100
        kind = "danger" if expense_ratio > 90 else "warning" if expense_ratio > 70 else "success"
        insights.append((f"שיעור ההוצאות מתוך ההכנסות בפועל הוא {pct(expense_ratio)}.", kind))

    if funding_group_col and funding_group_col in data.columns and C["unique_study"]:
        funding_summary = (
            data.groupby(funding_group_col)[C["unique_study"]]
            .sum()
            .sort_values(ascending=False)
        )

        if not funding_summary.empty:
            main_group = funding_summary.index[0]
            main_count = funding_summary.iloc[0]
            insights.append((f"קבוצת המימון הדומיננטית היא {main_group}, עם {number(main_count)} מחקרים.", "success"))

    if C["department"] and C["unique_study"] and C["department"] in data.columns:
        dept_top = (
            data.groupby(C["department"])[C["unique_study"]]
            .sum()
            .sort_values(ascending=False)
        )

        if not dept_top.empty:
            insights.append((f"המחלקה המובילה בכמות מחקרים היא {dept_top.index[0]} עם {number(dept_top.iloc[0])} מחקרים.", "success"))

    if C["pi"] and C["unique_study"] and C["pi"] in data.columns:
        pi_top = (
            data.groupby(C["pi"])[C["unique_study"]]
            .sum()
            .sort_values(ascending=False)
        )

        if not pi_top.empty:
            insights.append((f"החוקר המוביל בכמות מחקרים הוא {pi_top.index[0]} עם {number(pi_top.iloc[0])} מחקרים.", "success"))

    over_budget = len(data[data["סטטוס ניצול תקציב - מחושב"] == "חריגה"])
    low_recruit = len(data[data["סטטוס גיוס"].isin(["אין גיוס", "גיוס נמוך"])])

    if over_budget > 0:
        insights.append((f"{number(over_budget)} מחקרים נמצאים בחריגה תקציבית ודורשים בדיקה.", "danger"))

    if low_recruit > 0:
        insights.append((f"{number(low_recruit)} מחקרים עם גיוס נמוך או ללא גיוס.", "warning"))

    return insights


def plot_revenue_realization_by_year(data, year_col):
    if not year_col or year_col not in data.columns:
        return

    if "שיעור מימוש הכנסות" not in data.columns:
        return

    summary = (
        data.groupby(year_col, as_index=False)
        .agg(
            צפי_הכנסות=(C["expected_income"], "sum"),
            הכנסות_בפועל=(C["actual_income"], "sum")
        )
        .rename(columns={year_col: "שנה"})
    )

    summary["שיעור מימוש הכנסות"] = np.where(
        summary["צפי_הכנסות"] > 0,
        summary["הכנסות_בפועל"] / summary["צפי_הכנסות"] * 100,
        0
    )

    summary["תווית"] = summary["שיעור מימוש הכנסות"].apply(lambda x: f"{x:.1f}%")
    summary["שנה"] = summary["שנה"].astype(str)

    fig = px.bar(
        summary,
        x="שנה",
        y="שיעור מימוש הכנסות",
        text="תווית",
        title="שיעור מימוש הכנסות בפועל מתוך צפי לפי שנה",
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_color="#0f766e"
    )

    fig.update_layout(
        xaxis=dict(type="category", title="שנה"),
        yaxis=dict(title="שיעור מימוש הכנסות (%)", gridcolor="#e2e8f0"),
        bargap=0.38,
    )

    fig = plotly_base(fig, height=390)
    st.plotly_chart(fig, use_container_width=True)


def plot_funding_group_split(data):
    if "קבוצת מימון" not in data.columns or not C["unique_study"]:
        return

    summary = (
        data.groupby("קבוצת מימון", as_index=False)[C["unique_study"]]
        .sum()
        .rename(columns={C["unique_study"]: "מספר מחקרים"})
    )

    chart_card_start()
    plot_donut(
        summary,
        "קבוצת מימון",
        "מספר מחקרים",
        "התפלגות מחקרים לפי קבוצת מימון",
        height=380
    )
    chart_card_end()


def plot_expense_distribution(data, title="התפלגות הוצאות"):
    expense_cols = [
        C["salary_expenses"],
        C["materials_expenses"],
        C["fixed_expenses"],
        C["travel_expenses"],
        C["internal_expenses"],
    ]

    expense_cols = [col for col in expense_cols if col and col in data.columns]

    if not expense_cols:
        st.info("לא נמצאו עמודות הוצאות להצגת התפלגות.")
        return

    summary = pd.DataFrame({
        "סוג הוצאה": expense_cols,
        "סכום": [sum_col(data, col) for col in expense_cols]
    })

    summary = summary[summary["סכום"] > 0]

    if summary.empty:
        st.info("אין הוצאות להצגה בהתאם לסינון הנוכחי.")
        return

    chart_card_start()
    plot_donut(summary, "סוג הוצאה", "סכום", title, height=380)
    chart_card_end()


def plot_researcher_budget_execution(payment_details):
    cols = [
        D["budget_total"],
        D["purchase_commitments"],
        D["execution_total"],
        D["balance"],
    ]

    cols = [col for col in cols if col and col in payment_details.columns]

    if not cols:
        st.info("לא נמצאו עמודות תקציב / התחייבויות / ביצוע להצגה.")
        return

    summary = pd.DataFrame({
        "מדד": cols,
        "סכום": [sum_col(payment_details, col) for col in cols]
    })

    summary = summary[summary["סכום"] != 0]

    if summary.empty:
        st.info("אין נתונים תקציביים להצגה.")
        return

    summary["תווית"] = summary["סכום"].apply(compact_number)

    fig = px.bar(
        summary,
        x="מדד",
        y="סכום",
        text="תווית",
        title="תקציב מול התחייבויות רכש, ביצוע ויתרה",
        color="מדד",
        color_discrete_sequence=["#1d4ed8", "#f59e0b", "#ef4444", "#10b981"]
    )

    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        xaxis=dict(title=""),
        yaxis=dict(title="סכום", gridcolor="#e2e8f0"),
        showlegend=False,
    )

    fig = plotly_base(fig, height=390)
    st.plotly_chart(fig, use_container_width=True)


def risk_level(score):
    try:
        score = float(score)
    except Exception:
        return "לא ידוע"

    if score >= 6:
        return "סיכון גבוה"
    if score >= 3:
        return "סיכון בינוני"
    if score > 0:
        return "סיכון נמוך"
    return "תקין"


def recommended_action(row, balance_col=None):
    reasons = []

    if row.get("סטטוס ניצול תקציב - מחושב", "") == "חריגה":
        reasons.append("בדיקת חריגה תקציבית מול תקציב וניצול בפועל")

    if row.get("סטטוס ניצול תקציב - מחושב", "") == "קרוב לניצול מלא":
        reasons.append("בדיקת יתרת תקציב לפני אישור הוצאות נוספות")

    if row.get("סטטוס ניצול תקציב - מחושב", "") == "ניצול נמוך":
        reasons.append("בדיקת ניצול נמוך והאם נדרש עדכון פעילות/תקציב")

    if row.get("סטטוס גיוס", "") in ["אין גיוס", "גיוס נמוך"]:
        reasons.append("פנייה לחוקר לבדיקת קצב גיוס משתתפים")

    try:
        days = float(row.get("ימים לסיום", np.nan))
        if 0 <= days <= 60:
            reasons.append("בדיקת סגירת מחקר/ניצול יתרות לפני סיום")
    except Exception:
        pass

    if balance_col:
        try:
            balance = float(row.get(balance_col, np.nan))
            if balance < 0:
                reasons.append("בדיקת יתרה שלילית ופתיחת חריגה")
        except Exception:
            pass

    if not reasons:
        return "ללא פעולה מיידית"

    return " | ".join(reasons)


def badge_html(value):
    value = safe_value(value)

    if "🔴" in value or "חריגה" in value or "אדום" in value or "סיכון גבוה" in value:
        return f'<span class="badge badge-red">{escape(value)}</span>'

    if (
        "🟡" in value
        or "צהוב" in value
        or "ניצול נמוך" in value
        or "קרוב" in value
        or "גיוס נמוך" in value
        or "אין גיוס" in value
        or "סיכון בינוני" in value
        or "סיכון נמוך" in value
    ):
        return f'<span class="badge badge-yellow">{escape(value)}</span>'

    if "🟢" in value or "ירוק" in value or "תקין" in value:
        return f'<span class="badge badge-green">{escape(value)}</span>'

    return f'<span class="badge badge-blue">{escape(value)}</span>'


def format_cell(value, col, money_cols=None, percent_cols=None, number_cols=None, date_cols=None, badge_cols=None):
    money_cols = money_cols or []
    percent_cols = percent_cols or []
    number_cols = number_cols or []
    date_cols = date_cols or []
    badge_cols = badge_cols or []

    if col in badge_cols:
        return badge_html(value)

    if col in money_cols:
        return escape(money(value))

    if col in percent_cols:
        return escape(pct(value))

    if col in number_cols:
        return escape(number(value))

    if col in date_cols:
        try:
            dt = pd.to_datetime(value, errors="coerce")
            if pd.isna(dt):
                return ""
            return escape(dt.strftime("%d/%m/%Y"))
        except Exception:
            return ""

    return escape(safe_value(value))


def render_table(
    df,
    title=None,
    columns=None,
    max_rows=150,
    money_cols=None,
    percent_cols=None,
    number_cols=None,
    date_cols=None,
    badge_cols=None,
    height=430,
):
    if title:
        st.markdown(f'<div class="table-title">{escape(title)}</div>', unsafe_allow_html=True)

    if df is None or df.empty:
        st.info("אין נתונים להצגה בהתאם לבחירה הנוכחית.")
        return

    data = df.copy()

    if columns:
        columns = [c for c in columns if c and c in data.columns]
        if columns:
            data = data[columns]

    if data.empty:
        st.info("אין נתונים להצגה בהתאם לבחירה הנוכחית.")
        return

    if len(data) > max_rows:
        st.caption(f"מוצגות {max_rows} שורות מתוך {len(data):,}. ניתן להוריד את הדוח המלא לאקסל.")
        data = data.head(max_rows)

    headers = "".join([f"<th>{escape(str(col))}</th>" for col in data.columns])

    rows_html = []
    for _, row in data.iterrows():
        cells = []
        for col in data.columns:
            cells.append(
                f"<td>{format_cell(row[col], col, money_cols, percent_cols, number_cols, date_cols, badge_cols)}</td>"
            )
        rows_html.append("<tr>" + "".join(cells) + "</tr>")

    html = f"""
    <div class="table-wrap">
        <div class="table-scroll" style="max-height:{height}px;">
            <table class="prof-table">
                <thead>
                    <tr>{headers}</tr>
                </thead>
                <tbody>
                    {''.join(rows_html)}
                </tbody>
            </table>
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def kpi_grid(items, columns_per_row=5):
    if not items:
        return

    for start in range(0, len(items), columns_per_row):
        chunk = items[start:start + columns_per_row]
        cols = st.columns(len(chunk))

        for col, item in zip(cols, chunk):
            label, value = item
            with col:
                with st.container(border=True):
                    st.metric(label=str(label), value=str(value))


def identity_grid(items):
    html_items = []
    for label, value in items:
        html_items.append(
            f"""
            <div class="identity-card">
                <div class="identity-label">{escape(str(label))}</div>
                <div class="identity-value">{escape(safe_value(value))}</div>
            </div>
            """
        )

    html = f'<div class="identity-grid">{"".join(html_items)}</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_insights(title, insights):
    if not insights:
        return

    items_html = []

    for text, kind in insights:
        cls = "insight-item"
        if kind == "danger":
            cls += " insight-danger"
        elif kind == "warning":
            cls += " insight-warning"
        elif kind == "success":
            cls += " insight-success"

        items_html.append(f'<div class="{cls}">{escape(str(text))}</div>')

    html = f"""
    <div class="insight-box">
        <div class="insight-title">{escape(title)}</div>
        {''.join(items_html)}
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def page_header(title, subtitle):
    st.markdown(
        f"""
        <div class="page-header">
            <h2>{escape(title)}</h2>
            <p>{escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def explain_metrics():
    with st.expander("ℹ️ הסבר על המדדים בדשבורד", expanded=False):
        st.markdown(
            """
            <div style="direction:rtl; text-align:right; line-height:1.8;">

            **שיעור מימוש הכנסות**  
            מציג כמה מתוך צפי ההכנסות אכן התקבל בפועל.

            הנוסחה:
            <br>
            <b>הכנסות בפועל / צפי הכנסות × 100</b>

            לדוגמה: אם צפי ההכנסות הוא 100,000 ₪ וההכנסות בפועל הן 60,000 ₪, שיעור המימוש הוא 60%.

            ---

            **סטטוס ניצול תקציב**  
            מחושב לפי אחוז ניצול התקציב:
            <br>
            <b>סה״כ ניצול / תקציב × 100</b>

            | אחוז ניצול | סטטוס |
            |---:|---|
            | עד 20% | ניצול נמוך |
            | 20%–80% | תקין |
            | 80%–100% | קרוב לניצול מלא |
            | מעל 100% | חריגה |

            ---

            **סטטוס גיוס משתתפים**  
            מחושב לפי:
            <br>
            <b>משתתפים בפועל / צפי משתתפים × 100</b>

            ---

            **רמזור ניהולי**  
            הרמזור הוא אינדיקציה מהירה בלבד:
            <br>
            🔴 דורש טיפול / חריגה  
            🟡 דורש בדיקה  
            🟢 תקין

            ---

            **הפרדה בין מחקרי יזם לגרנט**  
            הדשבורד מסווג מחקרים לפי עמודת סוג המימון. אם מופיע ערך כמו "יזם" הוא יסווג כמחקר יזם. אם מופיע "גרנט" / "מענק" / "Grant" הוא יסווג כגרנט.

            </div>
            """,
            unsafe_allow_html=True
        )


def filter_select(df, label, col, key):
    if not col or col not in df.columns:
        return df, None

    values = sorted(df[col].dropna().astype(str).unique())

    if not values:
        return df.iloc[0:0], None

    selected = st.selectbox(label, values, key=key)
    return df[df[col].astype(str) == selected], selected


def filter_multiselect(df, label, col, key, default_all=True):
    if not col or col not in df.columns:
        return df

    values = sorted(df[col].dropna().astype(str).unique())

    if not values:
        return df.iloc[0:0]

    default = values if default_all else []

    selected = st.multiselect(label, values, default=default, key=key)

    if selected:
        return df[df[col].astype(str).isin(selected)]

    return df.iloc[0:0]


def shorten_label(value, max_len=26):
    text = safe_value(value)
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def chart_card_start():
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)


def chart_card_end():
    st.markdown("</div>", unsafe_allow_html=True)


def plotly_base(fig, height=420):
    fig.update_layout(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(size=13, color="#334155"),
        title=dict(x=0.5, font=dict(size=18, color="#0f172a")),
        margin=dict(l=40, r=40, t=80, b=60),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            title="",
        ),
    )
    return fig


def plot_vertical_bar(df, x, y, title, x_title=None, y_title=None, height=390):
    if df is None or df.empty or x not in df.columns or y not in df.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    plot_data = df.copy()
    plot_data[x] = plot_data[x].astype(str)
    plot_data["_text"] = plot_data[y].apply(compact_number)

    fig = px.bar(plot_data, x=x, y=y, text="_text", title=title)
    fig.update_traces(textposition="outside", cliponaxis=False, marker_color="#2563eb")
    fig.update_layout(
        xaxis=dict(type="category", title=x_title or x),
        yaxis=dict(title=y_title or y, gridcolor="#e2e8f0"),
        bargap=0.38,
    )
    fig = plotly_base(fig, height=height)
    st.plotly_chart(fig, use_container_width=True)


def plot_grouped_bar(df, x, y_cols, title, x_title=None, y_title=None, height=430):
    y_cols = [col for col in y_cols if col and col in df.columns]

    if df is None or df.empty or x not in df.columns or not y_cols:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    plot_data = df.copy()
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
        color_discrete_sequence=["#1d4ed8", "#38bdf8", "#ef4444", "#a78bfa", "#10b981"],
    )

    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        xaxis=dict(type="category", title=x_title or x),
        yaxis=dict(title=y_title or "סכום", gridcolor="#e2e8f0"),
        bargap=0.34,
    )
    fig = plotly_base(fig, height=height)
    st.plotly_chart(fig, use_container_width=True)


def plot_donut(df, names, values, title, height=390):
    if df is None or df.empty or names not in df.columns or values not in df.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.52,
        title=title,
        color_discrete_sequence=["#2563eb", "#06b6d4", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#64748b"],
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig = plotly_base(fig, height=height)
    st.plotly_chart(fig, use_container_width=True)


def plot_top10(df, label_col, value_col, title, x_title=None, height=430):
    if df is None or df.empty or label_col not in df.columns or value_col not in df.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    plot_data = df.copy()
    plot_data = plot_data.sort_values(value_col, ascending=True).tail(10)
    plot_data["שם מקוצר"] = plot_data[label_col].apply(lambda x: shorten_label(x, 28))
    plot_data["שם מלא"] = plot_data[label_col].astype(str)
    plot_data["תווית"] = plot_data[value_col].apply(compact_number)

    dynamic_height = max(height, len(plot_data) * 48 + 150)

    fig = px.bar(
        plot_data,
        x=value_col,
        y="שם מקוצר",
        orientation="h",
        text="תווית",
        title=title,
        hover_data={"שם מלא": True, value_col: ":,.0f", "שם מקוצר": False},
    )

    fig.update_traces(textposition="outside", cliponaxis=False, marker_color="#2563eb")
    fig.update_layout(
        xaxis=dict(title=x_title or value_col, gridcolor="#e2e8f0"),
        yaxis=dict(title="", automargin=True),
        showlegend=False,
        margin=dict(l=170, r=85, t=80, b=50),
    )
    fig = plotly_base(fig, height=dynamic_height)
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

    others = [s for s in xls.sheet_names if s != studies_sheet]
    return others[0] if others else studies_sheet


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown("## 📊 מחקרים קליניים")
    st.caption(APP_VERSION)

    page = st.radio(
        "ניווט",
        [
            "📌 תקציר מנהלים",
            "🏥 כלל בית החולים",
            "🏢 מחלקות",
            "👩‍⚕️ חוקרים",
            "🏭 יזמים",
            "🚦 סיכונים ותקציב",
            "🧾 דוח חוקר",
            "💳 מעקב דרישות תשלום",
        ],
        label_visibility="collapsed",
    )


# ============================================================
# HEADER + UPLOAD
# ============================================================

st.markdown(
    f"""
    <div class="hero">
        <h1>📊 דשבורד ניהולי למחקרים קליניים</h1>
        <p>תצוגת הנהלה למחקרים, תקציבים, הכנסות, הוצאות, סיכונים, חוקרים, מחלקות ויזמים | {APP_VERSION}</p>
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
# CLEANING + CALCULATIONS
# ============================================================

numeric_studies_cols = [
    C["expected_income"], C["actual_income"], C["total_expenses"],
    C["salary_expenses"], C["materials_expenses"], C["fixed_expenses"],
    C["travel_expenses"], C["internal_expenses"], C["expected_participants"],
    C["actual_participants"], C["unique_study"], C["unique_researcher"],
    C["budget"], C["overhead"], C["commitment"], C["execution"],
    C["utilization_total"], C["utilization_pct"], C["balance"], C["unreserved_balance"],
]

numeric_details_cols = [
    D["budget_total"], D["purchase_commitments"], D["execution_total"], D["balance"],
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
# FUNDING GROUP + REVENUE REALIZATION
# ============================================================

if C["funding_type"] and C["funding_type"] in df.columns:
    df["קבוצת מימון"] = df[C["funding_type"]].apply(classify_funding_group)
else:
    df["קבוצת מימון"] = "לא סווג"

df = add_revenue_realization(df, C["expected_income"], C["actual_income"])

# ============================================================
# DISPLAY COLUMNS
# ============================================================

study_summary_cols = [
    C["study_id"], C["protocol"], C["pi"], C["department"], C["sponsor"],
    C["study_type"], C["funding_type"], "קבוצת מימון", C["approval_year"],
    C["expected_income"], C["actual_income"], "שיעור מימוש הכנסות",
    C["total_expenses"], C["expected_participants"], C["actual_participants"],
    "% גיוס משתתפים", "% ניצול תקציב - מחושב",
    "סטטוס ניצול תקציב - מחושב", "רמזור ניהולי",
]

budget_status_cols = [
    C["study_id"], C["protocol"], C["pi"], C["department"], C["sponsor"],
    C["funding_type"], "קבוצת מימון", C["wbs"], C["budget_name"],
    C["budget"], C["utilization_total"], "% ניצול תקציב - מחושב",
    C["balance"], C["unreserved_balance"], C["end_date"],
    "ימים לסיום", "סטטוס גיוס", "סטטוס ניצול תקציב - מחושב",
    "רמזור ניהולי",
]

researcher_short_cols = [
    C["study_id"], C["protocol"], C["sponsor"], C["funding_type"],
    "קבוצת מימון", C["wbs"], C["budget_name"],
    C["budget"], "% ניצול תקציב - מחושב", C["balance"],
    "סטטוס ניצול תקציב - מחושב", "רמזור ניהולי",
]

researcher_identity_cols = [
    C["study_id"], C["protocol"], C["pi"], C["department"], C["site"],
    C["sponsor"], C["study_type"], C["phase"], C["start_date"], C["end_date"],
    C["budget_name"], C["budget_owner"], C["wbs"], C["contract"], C["budget"],
    C["execution"], C["commitment"], C["utilization_total"], C["balance"],
    C["unreserved_balance"], "% ניצול תקציב - מחושב",
    C["expected_participants"], C["actual_participants"], "% גיוס משתתפים",
    "סטטוס גיוס", "ציון סיכון", "רמת סיכון", "פעולה מומלצת", "רמזור ניהולי",
]

payment_cols = [
    D["wbs"], D["study_id"], D["protocol"], D["pi_name"], D["site"],
    D["budget_category"], D["commitment_group"], D["commitment_group_desc"],
    D["description"], D["budget_total"], D["purchase_commitments"],
    D["execution_total"], D["balance"],
]

money_cols = [
    C["expected_income"], C["actual_income"], C["total_expenses"], C["budget"],
    C["execution"], C["commitment"], C["utilization_total"], C["balance"],
    C["unreserved_balance"], D["budget_total"], D["purchase_commitments"],
    D["execution_total"], D["balance"],
]

percent_cols = ["% ניצול תקציב - מחושב", "% גיוס משתתפים", "שיעור מימוש הכנסות"]
number_cols = [C["expected_participants"], C["actual_participants"], "ימים לסיום", "ציון סיכון"]
date_cols = [C["approval_date"], C["start_date"], C["end_date"]]
badge_cols = ["סטטוס ניצול תקציב - מחושב", "סטטוס גיוס", "רמזור ניהולי", "קבוצת מימון"]


# ============================================================
# INSIGHTS
# ============================================================

def build_general_insights(data):
    return build_clean_insights(data, "קבוצת מימון")


# ============================================================
# PAGES
# ============================================================

if page == "📌 תקציר מנהלים":
    page_header(
        "📌 תקציר מנהלים",
        "תמונת מצב מרוכזת להנהלה: מחקרים, הכנסות, הוצאות, סיכונים ומחקרים הדורשים טיפול."
    )
    explain_metrics()

    kpi_grid(
        [
            ("סה״כ מחקרים", number(count_unique_studies(df, C["unique_study"], C["study_id"]))),
            ("מספר חוקרים", number(df[C["pi"]].nunique() if C["pi"] else 0)),
            ("צפי הכנסות", money(sum_col(df, C["expected_income"]))),
            ("הכנסות בפועל", money(sum_col(df, C["actual_income"]))),
            ("מחקרים בסיכון גבוה", number(len(df[df["רמת סיכון"] == "סיכון גבוה"]))),
        ]
    )

    render_insights("תובנות מרכזיות", build_general_insights(df))

    c1, c2 = st.columns(2)

    with c1:
        if C["approval_year"]:
            if C["unique_study"]:
                yearly = (
                    df.groupby(C["approval_year"], as_index=False)[C["unique_study"]]
                    .sum()
                    .rename(columns={C["approval_year"]: "שנה", C["unique_study"]: "מספר מחקרים"})
                )
            else:
                yearly = (
                    df.groupby(C["approval_year"], as_index=False)
                    .size()
                    .rename(columns={C["approval_year"]: "שנה", "size": "מספר מחקרים"})
                )

            chart_card_start()
            plot_vertical_bar(yearly, "שנה", "מספר מחקרים", "מגמת מחקרים לפי שנה", "שנה", "מספר מחקרים", height=360)
            chart_card_end()

    with c2:
        risk_summary = (
            df.groupby("רמת סיכון", as_index=False)
            .size()
            .rename(columns={"size": "מספר מחקרים"})
        )

        chart_card_start()
        plot_donut(risk_summary, "רמת סיכון", "מספר מחקרים", "התפלגות רמות סיכון", height=360)
        chart_card_end()

    high_risk = df[df["רמת סיכון"] == "סיכון גבוה"].sort_values("ציון סיכון", ascending=False)

    render_table(
        high_risk,
        title="מחקרים בסיכון גבוה לטיפול",
        columns=budget_status_cols,
        money_cols=money_cols,
        percent_cols=percent_cols,
        number_cols=number_cols,
        date_cols=date_cols,
        badge_cols=badge_cols,
        height=390,
    )


elif page == "🏥 כלל בית החולים":
    page_header(
        "🏥 כלל בית החולים",
        "ניתוח רוחבי של כלל המחקרים לפי שנים, סוגי מימון, הכנסות, הוצאות וחוקרים מובילים."
    )
    explain_metrics()

    hospital = df.copy()

    with st.container(border=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            hospital = filter_multiselect(hospital, "שנה", C["approval_year"], key="hospital_year")
        with f2:
            hospital = filter_multiselect(hospital, "סוג מימון", C["funding_type"], key="hospital_funding")
        with f3:
            hospital = filter_multiselect(hospital, "סוג מחקר", C["study_type"], key="hospital_type")

    kpi_grid(
        [
            ("סה״כ מחקרים", number(count_unique_studies(hospital, C["unique_study"], C["study_id"]))),
            ("מספר חוקרים", number(hospital[C["pi"]].nunique() if C["pi"] else 0)),
            ("צפי הכנסות", money(sum_col(hospital, C["expected_income"]))),
            ("הכנסות בפועל", money(sum_col(hospital, C["actual_income"]))),
            ("סך הוצאות", money(sum_col(hospital, C["total_expenses"]))),
        ]
    )

    render_insights("תובנות כלל בית החולים", build_general_insights(hospital))

    if C["approval_year"]:
        if C["unique_study"]:
            yearly_count = (
                hospital.groupby(C["approval_year"], as_index=False)[C["unique_study"]]
                .sum()
                .rename(columns={C["approval_year"]: "שנה", C["unique_study"]: "מספר מחקרים"})
            )
        else:
            yearly_count = (
                hospital.groupby(C["approval_year"], as_index=False)
                .size()
                .rename(columns={C["approval_year"]: "שנה", "size": "מספר מחקרים"})
            )

        chart_card_start()
        plot_vertical_bar(yearly_count, "שנה", "מספר מחקרים", "סה״כ מחקרים לפי שנה", "שנה", "מספר מחקרים")
        chart_card_end()

        money_year_cols = [C["expected_income"], C["actual_income"], C["total_expenses"], C["overhead"]]
        money_year_cols = [col for col in money_year_cols if col]

        if money_year_cols:
            yearly_money = (
                hospital.groupby(C["approval_year"], as_index=False)[money_year_cols]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )

            chart_card_start()
            plot_grouped_bar(yearly_money, "שנה", money_year_cols, "צפי הכנסות, הכנסות בפועל, הוצאות ותקורה לפי שנה", "שנה", "סכום")
            chart_card_end()

            chart_card_start()
            plot_revenue_realization_by_year(hospital, C["approval_year"])
            chart_card_end()
            
            plot_funding_group_split(hospital)

    
    c1, c2 = st.columns(2)

    with c1:
        if C["funding_type"] and C["unique_study"]:
            funding = (
                hospital.groupby(C["funding_type"], as_index=False)[C["unique_study"]]
                .sum()
                .rename(columns={C["funding_type"]: "סוג מימון", C["unique_study"]: "מספר מחקרים"})
            )

            chart_card_start()
            plot_donut(funding, "סוג מימון", "מספר מחקרים", "התפלגות מחקרים לפי סוג מימון")
            chart_card_end()

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

            distribution = (
                researcher_counts.groupby("טווח מחקרים לחוקר", as_index=False, observed=False)
                .size()
                .rename(columns={"size": "מספר חוקרים"})
            )

            chart_card_start()
            plot_donut(distribution, "טווח מחקרים לחוקר", "מספר חוקרים", "התפלגות כמות מחקרים לחוקר")
            chart_card_end()

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

            chart_card_start()
            plot_top10(top_pi_count, "חוקר ראשי", "מספר מחקרים", "Top 10 חוקרים לפי כמות מחקרים", "מספר מחקרים")
            chart_card_end()

    with c4:
        if C["pi"] and C["expected_income"]:
            top_pi_income = (
                hospital.groupby(C["pi"], as_index=False)[C["expected_income"]]
                .sum()
                .sort_values(C["expected_income"], ascending=False)
                .head(10)
                .rename(columns={C["pi"]: "חוקר ראשי", C["expected_income"]: "צפי הכנסות"})
            )

            chart_card_start()
            plot_top10(top_pi_income, "חוקר ראשי", "צפי הכנסות", "Top 10 חוקרים לפי צפי הכנסות", "צפי הכנסות")
            chart_card_end()


elif page == "🏢 מחלקות":
    page_header(
        "🏢 מחלקות",
        "דוח מחלקתי ממוקד: מחקרים, הכנסות, סיכונים ופעולות מומלצות לפי מחלקה."
    )
    explain_metrics()

    dept = df.copy()

    with st.container(border=True):
        f1, f2 = st.columns(2)
        with f1:
            dept, selected_dept = filter_select(dept, "מחלקה", C["department"], key="dept_select")
        with f2:
            dept = filter_multiselect(dept, "שנה", C["approval_year"], key="dept_year")

    kpi_grid(
        [
            ("מחלקה", selected_dept or "-"),
            ("מספר מחקרים", number(count_unique_studies(dept, C["unique_study"], C["study_id"]))),
            ("צפי הכנסות", money(sum_col(dept, C["expected_income"]))),
            ("הכנסות בפועל", money(sum_col(dept, C["actual_income"]))),
            ("מחקרים בסיכון גבוה", number(len(dept[dept["רמת סיכון"] == "סיכון גבוה"]))),
        ]
    )

    render_insights("תובנות מחלקה", build_general_insights(dept))

    c1, c2 = st.columns(2)

with c1:
    plot_funding_group_split(dept)

with c2:
    chart_card_start()
    plot_revenue_realization_by_year(dept, C["approval_year"])
    chart_card_end()

    if C["approval_year"]:
        dept_money_cols = [C["expected_income"], C["actual_income"], C["total_expenses"]]
        dept_money_cols = [col for col in dept_money_cols if col]

        if dept_money_cols:
            dept_year = (
                dept.groupby(C["approval_year"], as_index=False)[dept_money_cols]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )

            chart_card_start()
            plot_grouped_bar(dept_year, "שנה", dept_money_cols, "הכנסות והוצאות לפי שנה במחלקה", "שנה", "סכום")
            chart_card_end()

    render_table(
        dept,
        title="טבלת מחקרים במחלקה",
        columns=study_summary_cols,
        money_cols=money_cols,
        percent_cols=percent_cols,
        number_cols=number_cols,
        date_cols=date_cols,
        badge_cols=badge_cols,
        height=430,
    )

    dept_excel = download_excel_openpyxl({"department_report": dept})
    st.download_button(
        "⬇️ הורדת דוח מחלקה לאקסל",
        dept_excel,
        "department_report.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


elif page == "👩‍⚕️ חוקרים":
    page_header(
        "👩‍⚕️ חוקרים",
        "ניתוח לפי חוקר ראשי: מחקרים, הכנסות, הוצאות, סיכונים ופעולות נדרשות."
    )
    explain_metrics()

    pi_df = df.copy()

    with st.container(border=True):
        f1, f2 = st.columns(2)
        with f1:
            pi_df, selected_pi = filter_select(pi_df, "חוקר ראשי", C["pi"], key="pi_select")
        with f2:
            pi_df = filter_multiselect(pi_df, "שנה", C["approval_year"], key="pi_year")

    kpi_grid(
        [
            ("חוקר", selected_pi or "-"),
            ("מספר מחקרים", number(count_unique_studies(pi_df, C["unique_study"], C["study_id"]))),
            ("צפי הכנסות", money(sum_col(pi_df, C["expected_income"]))),
            ("הכנסות בפועל", money(sum_col(pi_df, C["actual_income"]))),
            ("מחקרים בסיכון גבוה", number(len(pi_df[pi_df["רמת סיכון"] == "סיכון גבוה"]))),
        ]
    )

    render_insights("תובנות חוקר", build_general_insights(pi_df))

c1, c2 = st.columns(2)

with c1:
    plot_funding_group_split(pi_df)

with c2:
    plot_expense_distribution(pi_df, "התפלגות הוצאות לחוקר")

    if C["approval_year"]:
        pi_money_cols = [C["expected_income"], C["actual_income"], C["total_expenses"]]
        pi_money_cols = [col for col in pi_money_cols if col]

        if pi_money_cols:
            pi_year = (
                pi_df.groupby(C["approval_year"], as_index=False)[pi_money_cols]
                .sum()
                .rename(columns={C["approval_year"]: "שנה"})
            )

            chart_card_start()
            plot_grouped_bar(pi_year, "שנה", pi_money_cols, "הכנסות מול הוצאות לפי שנה לחוקר", "שנה", "סכום")
            chart_card_end()

    render_table(
        pi_df,
        title="טבלת מחקרים לחוקר",
        columns=study_summary_cols,
        money_cols=money_cols,
        percent_cols=percent_cols,
        number_cols=number_cols,
        date_cols=date_cols,
        badge_cols=badge_cols,
        height=430,
    )


elif page == "🏭 יזמים":
    page_header(
        "🏭 יזמים",
        "ניתוח לפי יזם: כמות מחקרים, צפי הכנסות, הכנסות בפועל והוצאות."
    )

    sponsor_df = df.copy()

    with st.container(border=True):
        f1, f2 = st.columns(2)
        with f1:
            sponsor_df = filter_multiselect(sponsor_df, "יזם", C["sponsor"], key="sponsor_select")
        with f2:
            sponsor_df = filter_multiselect(sponsor_df, "שנה", C["approval_year"], key="sponsor_year")

    if C["sponsor"]:
        sponsor_summary = sponsor_df.groupby(C["sponsor"], as_index=False).agg(מספר_רשומות=(C["sponsor"], "size"))

        if C["unique_study"]:
            sponsor_count = (
                sponsor_df.groupby(C["sponsor"], as_index=False)[C["unique_study"]]
                .sum()
                .rename(columns={C["unique_study"]: "מספר מחקרים"})
            )
            sponsor_summary = sponsor_summary.merge(sponsor_count, on=C["sponsor"], how="left")
        else:
            sponsor_summary["מספר מחקרים"] = sponsor_summary["מספר_רשומות"]

        if C["expected_income"]:
            sponsor_income = (
                sponsor_df.groupby(C["sponsor"], as_index=False)[C["expected_income"]]
                .sum()
                .rename(columns={C["expected_income"]: "צפי הכנסות"})
            )
            sponsor_summary = sponsor_summary.merge(sponsor_income, on=C["sponsor"], how="left")

        if C["actual_income"]:
            sponsor_actual = (
                sponsor_df.groupby(C["sponsor"], as_index=False)[C["actual_income"]]
                .sum()
                .rename(columns={C["actual_income"]: "הכנסות בפועל"})
            )
            sponsor_summary = sponsor_summary.merge(sponsor_actual, on=C["sponsor"], how="left")

        if C["total_expenses"]:
            sponsor_exp = (
                sponsor_df.groupby(C["sponsor"], as_index=False)[C["total_expenses"]]
                .sum()
                .rename(columns={C["total_expenses"]: "סך הוצאות"})
            )
            sponsor_summary = sponsor_summary.merge(sponsor_exp, on=C["sponsor"], how="left")

        sponsor_summary = sponsor_summary.rename(columns={C["sponsor"]: "יזם"})
        sponsor_summary = sponsor_summary.sort_values("מספר מחקרים", ascending=False)

        kpi_grid(
            [
                ("מספר יזמים", number(sponsor_summary["יזם"].nunique())),
                ("סה״כ מחקרים", number(sponsor_summary["מספר מחקרים"].sum())),
                ("צפי הכנסות", money(sponsor_summary["צפי הכנסות"].sum()) if "צפי הכנסות" in sponsor_summary.columns else "0 ₪"),
                ("הכנסות בפועל", money(sponsor_summary["הכנסות בפועל"].sum()) if "הכנסות בפועל" in sponsor_summary.columns else "0 ₪"),
                ("סך הוצאות", money(sponsor_summary["סך הוצאות"].sum()) if "סך הוצאות" in sponsor_summary.columns else "0 ₪"),
            ]
        )

        c1, c2 = st.columns(2)

        with c1:
            chart_card_start()
            plot_top10(sponsor_summary, "יזם", "מספר מחקרים", "Top 10 יזמים לפי כמות מחקרים", "מספר מחקרים")
            chart_card_end()

        with c2:
            if "צפי הכנסות" in sponsor_summary.columns:
                chart_card_start()
                plot_top10(sponsor_summary, "יזם", "צפי הכנסות", "Top 10 יזמים לפי צפי הכנסות", "צפי הכנסות")
                chart_card_end()

        render_table(
            sponsor_summary,
            title="טבלת סיכום יזמים",
            money_cols=["צפי הכנסות", "הכנסות בפועל", "סך הוצאות"],
            number_cols=["מספר מחקרים"],
            height=430,
        )


elif page == "🚦 סיכונים ותקציב":
    page_header(
        "🚦 סיכונים ותקציב",
        "דוח התרעות ניהולי: חריגות, סיכון גבוה, גיוס נמוך, ניצול תקציבי וסיום קרוב."
    )
    explain_metrics()

    status_df = df.copy()

    with st.container(border=True):
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
            status_df = filter_multiselect(status_df, "רמת סיכון", "רמת סיכון", key="status_risk")
        with f6:
            status_df = filter_multiselect(status_df, "סטטוס גיוס", "סטטוס גיוס", key="status_recruit")

    over_budget = status_df[status_df["סטטוס ניצול תקציב - מחושב"] == "חריגה"]
    high_util = status_df[status_df["סטטוס ניצול תקציב - מחושב"] == "קרוב לניצול מלא"]
    low_util = status_df[status_df["סטטוס ניצול תקציב - מחושב"] == "ניצול נמוך"]
    low_recruit = status_df[status_df["סטטוס גיוס"].isin(["אין גיוס", "גיוס נמוך"])]
    high_risk = status_df[status_df["רמת סיכון"] == "סיכון גבוה"]
    ending_soon = status_df[(status_df["ימים לסיום"] >= 0) & (status_df["ימים לסיום"] <= 60)]

    kpi_grid(
        [
            ("🔴 מחקרים בחריגה", number(len(over_budget))),
            ("🔴 סיכון גבוה", number(len(high_risk))),
            ("🟡 קרוב לניצול מלא", number(len(high_util))),
            ("🟡 גיוס נמוך / אין גיוס", number(len(low_recruit))),
            ("🟡 מסתיימים תוך 60 יום", number(len(ending_soon))),
        ]
    )

    c1, c2 = st.columns(2)

    with c1:
        risk_summary = (
            status_df.groupby("רמת סיכון", as_index=False)
            .size()
            .rename(columns={"size": "מספר מחקרים"})
        )

        chart_card_start()
        plot_donut(risk_summary, "רמת סיכון", "מספר מחקרים", "התפלגות רמות סיכון")
        chart_card_end()

    with c2:
        status_summary = (
            status_df.groupby("סטטוס ניצול תקציב - מחושב", as_index=False)
            .size()
            .rename(columns={"size": "מספר מחקרים"})
        )

        chart_card_start()
        plot_donut(status_summary, "סטטוס ניצול תקציב - מחושב", "מספר מחקרים", "התפלגות סטטוס ניצול תקציבי")
        chart_card_end()

    alert_page = st.radio(
        "בחרי סוג התרעה להצגה",
        [
            "🔴 סיכון גבוה",
            "🔴 חריגה תקציבית",
            "🟡 קרוב לניצול מלא",
            "🟡 ניצול נמוך",
            "🟡 גיוס נמוך",
            "🟡 סיום קרוב",
            "📋 כל הסטטוסים",
        ],
        horizontal=True,
    )

    if alert_page == "🔴 סיכון גבוה":
        table_data = high_risk
        title = "מחקרים בסיכון גבוה"
    elif alert_page == "🔴 חריגה תקציבית":
        table_data = over_budget
        title = "מחקרים בחריגה תקציבית"
    elif alert_page == "🟡 קרוב לניצול מלא":
        table_data = high_util
        title = "מחקרים קרובים לניצול מלא"
    elif alert_page == "🟡 ניצול נמוך":
        table_data = low_util
        title = "מחקרים בניצול נמוך"
    elif alert_page == "🟡 גיוס נמוך":
        table_data = low_recruit
        title = "מחקרים עם גיוס נמוך / ללא גיוס"
    elif alert_page == "🟡 סיום קרוב":
        table_data = ending_soon
        title = "מחקרים שמסתיימים תוך 60 יום"
    else:
        table_data = status_df
        title = "טבלת סטטוס ניהול תקציב"

    render_table(
        table_data,
        title,
        budget_status_cols,
        money_cols=money_cols,
        percent_cols=percent_cols,
        number_cols=number_cols,
        date_cols=date_cols,
        badge_cols=badge_cols,
    )

    risk_excel = download_excel_openpyxl({"risk_report": status_df})
    st.download_button(
        "⬇️ הורדת דוח סטטוס וסיכונים לאקסל",
        risk_excel,
        "risk_status_report.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


elif page == "🧾 דוח חוקר":
    page_header(
        "🧾 דוח חוקר",
        "בחירת חוקר, הצגת רשימת מחקרים מקוצרת ותעודת זהות מפורטת למחקר נבחר."
    )
    explain_metrics()

    r_df = df.copy()

    with st.container(border=True):
        f1, f2 = st.columns(2)
        with f1:
            r_df, selected_researcher = filter_select(r_df, "חוקר", C["pi"], key="researcher_sheet_select")
        with f2:
            r_df = filter_multiselect(r_df, "שנה", C["approval_year"], key="researcher_sheet_year")

    kpi_grid(
        [
            ("חוקר", selected_researcher or "-"),
            ("מספר מחקרים", number(count_unique_studies(r_df, C["unique_study"], C["study_id"]))),
            ("תקציב כולל", money(sum_col(r_df, C["budget"]))),
            ("סה״כ ניצול", money(sum_col(r_df, C["utilization_total"]))),
            ("מחקרים בסיכון גבוה", number(len(r_df[r_df["רמת סיכון"] == "סיכון גבוה"]))),
        ]
    )

    render_table(
        r_df,
        title="רשימת מחקרים מקוצרת לחוקר",
        columns=researcher_short_cols,
        money_cols=money_cols,
        percent_cols=percent_cols,
        number_cols=number_cols,
        date_cols=date_cols,
        badge_cols=badge_cols,
        height=320,
    )

    # ============================================================
# RESEARCHER PAYMENT SUMMARY
# ============================================================

researcher_payment_source = r_df.copy()

study_ids_for_researcher = (
    researcher_payment_source[C["study_id"]].dropna().astype(str).unique().tolist()
    if C["study_id"] and C["study_id"] in researcher_payment_source.columns
    else []
)

protocols_for_researcher = (
    researcher_payment_source[C["protocol"]].dropna().astype(str).unique().tolist()
    if C["protocol"] and C["protocol"] in researcher_payment_source.columns
    else []
)

researcher_payment_details = details.copy()
payment_masks = []

if D["study_id"] and study_ids_for_researcher:
    payment_masks.append(researcher_payment_details[D["study_id"]].astype(str).isin(study_ids_for_researcher))

if D["protocol"] and protocols_for_researcher:
    payment_masks.append(researcher_payment_details[D["protocol"]].astype(str).isin(protocols_for_researcher))

if D["pi_name"] and selected_researcher:
    payment_masks.append(researcher_payment_details[D["pi_name"]].astype(str) == str(selected_researcher))

if payment_masks:
    combined_payment_mask = payment_masks[0]
    for mask in payment_masks[1:]:
        combined_payment_mask = combined_payment_mask | mask
    researcher_payment_details = researcher_payment_details[combined_payment_mask]

chart_card_start()
plot_researcher_budget_execution(researcher_payment_details)
chart_card_end()

    if C["study_id"] and not r_df.empty:
        page_header(
            "תעודת זהות למחקר",
            "בחרי מחקר מתוך רשימת המחקרים של החוקר כדי לפתוח כרטיס מחקר מפורט."
        )

        study_options = sorted(r_df[C["study_id"]].dropna().astype(str).unique())
        selected_study = st.selectbox("בחרי מחקר לפתיחת תעודת זהות", study_options, key="identity_study_select")

        selected_study_df = r_df[r_df[C["study_id"]].astype(str) == selected_study]

        if not selected_study_df.empty:
            row = selected_study_df.iloc[0]

            identity_grid(
                [
                    ("מספר הלסינקי", row.get(C["study_id"], "")),
                    ("מספר פרוטוקול", row.get(C["protocol"], "") if C["protocol"] else ""),
                    ("חוקר ראשי", row.get(C["pi"], "") if C["pi"] else ""),
                    ("מחלקה", row.get(C["department"], "") if C["department"] else ""),
                    ("יזם", row.get(C["sponsor"], "") if C["sponsor"] else ""),
                    ("אלמנט WBS", row.get(C["wbs"], "") if C["wbs"] else ""),
                    ("שם תקציב", row.get(C["budget_name"], "") if C["budget_name"] else ""),
                    ("רמת סיכון", row.get("רמת סיכון", "")),
                    ("פעולה מומלצת", row.get("פעולה מומלצת", "")),
                    ("תקציב", money(row.get(C["budget"], 0)) if C["budget"] else "0 ₪"),
                    ("סה״כ ניצול", money(row.get(C["utilization_total"], 0)) if C["utilization_total"] else "0 ₪"),
                    ("יתרה לניצול", money(row.get(C["balance"], 0)) if C["balance"] else "0 ₪"),
                    ("% ניצול", pct(row.get("% ניצול תקציב - מחושב", 0))),
                    ("צפי משתתפים", number(row.get(C["expected_participants"], 0)) if C["expected_participants"] else "0"),
                    ("משתתפים בפועל", number(row.get(C["actual_participants"], 0)) if C["actual_participants"] else "0"),
                    ("% גיוס", pct(row.get("% גיוס משתתפים", 0))),
                ]
            )

            render_table(
                selected_study_df,
                title="פרטים מלאים למחקר שנבחר",
                columns=researcher_identity_cols,
                money_cols=money_cols,
                percent_cols=percent_cols,
                number_cols=number_cols,
                date_cols=date_cols,
                badge_cols=badge_cols,
                height=330,
            )


elif page == "💳 מעקב דרישות תשלום":
    page_header(
        "💳 מעקב דרישות תשלום",
        "מעקב תקציבי לפי חוקר/מחקר: תקציב, התחייבויות, ביצוע, יתרה ופירוט לפי קטגוריות."
    )

    payment_source = df.copy()

    with st.container(border=True):
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
        payment_details = filter_multiselect(payment_details, "מחקר", D["study_id"], key="payment_study_filter")

    kpi_grid(
        [
            ("חוקר", payment_researcher or "-"),
            ("סה״כ תקציב", money(sum_col(payment_details, D["budget_total"]))),
            ("התחייבויות רכש", money(sum_col(payment_details, D["purchase_commitments"]))),
            ("סה״כ ביצוע", money(sum_col(payment_details, D["execution_total"]))),
            ("יתרה לניצול", money(sum_col(payment_details, D["balance"]))),
        ]
    )

    if D["budget_category"]:
        summary_cols = [D["budget_total"], D["purchase_commitments"], D["execution_total"], D["balance"]]
        summary_cols = [col for col in summary_cols if col]

        if summary_cols:
            category_summary = (
                payment_details.groupby(D["budget_category"], as_index=False)[summary_cols]
                .sum()
                .rename(columns={D["budget_category"]: "קטגוריית סעיף תקציבי"})
            )

            c1, c2 = st.columns([1, 1])

            with c1:
                render_table(
                    category_summary,
                    title="סיכום לפי קטגוריית סעיף תקציבי",
                    money_cols=summary_cols,
                    height=310,
                )

            with c2:
                chart_card_start()
                plot_grouped_bar(
                    category_summary,
                    "קטגוריית סעיף תקציבי",
                    summary_cols,
                    "תקציב, התחייבויות, ביצוע ויתרה לפי קטגוריה",
                    "קטגוריה",
                    "סכום",
                    height=360,
                )
                chart_card_end()

    if D["wbs"]:
        wbs_summary_cols = [D["budget_total"], D["purchase_commitments"], D["execution_total"], D["balance"]]
        wbs_summary_cols = [col for col in wbs_summary_cols if col]

        if wbs_summary_cols:
            wbs_summary = (
                payment_details.groupby(D["wbs"], as_index=False)[wbs_summary_cols]
                .sum()
                .rename(columns={D["wbs"]: "אלמנט WBS"})
            )

            render_table(
                wbs_summary,
                title="סיכום לפי WBS",
                money_cols=wbs_summary_cols,
                height=300,
            )

    render_table(
        payment_details,
        title="טבלת מעקב דרישות תשלום",
        columns=payment_cols,
        money_cols=money_cols,
        percent_cols=percent_cols,
        number_cols=number_cols,
        date_cols=date_cols,
        badge_cols=badge_cols,
        height=430,
    )

    payments_excel = download_excel_openpyxl({"payment_tracking": payment_details})

    st.download_button(
        "⬇️ הורדת מעקב דרישות תשלום לאקסל",
        payments_excel,
        "researcher_payment_tracking.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
