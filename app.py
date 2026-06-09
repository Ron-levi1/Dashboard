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

APP_VERSION = "v17-tiny-table-metric-fixes-keep-design-2026-06-09"

# ============================================================
# GLOBAL RTL + PROFESSIONAL CSS
# ============================================================

st.markdown(
    """
<style>
:root {
    --bg: #f5f7fb;
    --card: #ffffff;
    --text: #111827;
    --muted: #6b7280;
    --border: #e1e7ef;

    --navy: #102033;
    --navy-soft: #172b43;
    --blue: #245c9f;
    --blue-soft: #eaf2fb;
    --teal: #167c80;
    --teal-dark: #0f5f63;

    --green: #15803d;
    --green-bg: #ecfdf3;
    --amber: #b7791f;
    --amber-bg: #fff7e6;
    --red: #b42318;
    --red-bg: #fff1f0;
    --purple: #5b4b8a;
    --purple-bg: #f3f0ff;
}

html, body, [class*="css"] {
    direction: rtl !important;
    text-align: right !important;
    font-family: Calibri, Arial, sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

* {
    font-family: Calibri, Arial, sans-serif !important;
}

/* תיקון חשוב: מחזיר ל-Streamlit את פונט האייקונים כדי שלא יופיע טקסט כמו d_double_arrow_left / keyboard_arrow_down */
span[class*="material"],
span[class*="Material"],
button[data-testid="stBaseButton-headerNoPadding"] span,
button[data-testid="stBaseButton-header"] span,
[data-testid="stSidebarCollapseButton"] span,
[data-baseweb="select"] svg,
[data-baseweb="select"] span[class*="icon"],
[data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons", sans-serif !important;
    font-weight: normal !important;
    font-style: normal !important;
    line-height: 1 !important;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2.2rem !important;
    max-width: 1620px !important;
}

h1, h2, h3, h4, h5, h6, p, label, span {
    direction: rtl;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #102033 0%, #172b43 100%) !important;
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
    background: rgba(255,255,255,.07);
    border-radius: 12px;
    padding: 8px 10px;
    margin-bottom: 6px;
}

.hero {
    background: linear-gradient(135deg,#102033 0%,#245c9f 54%,#167c80 100%);
    color: white;
    padding: 34px 38px;
    border-radius: 28px;
    margin-bottom: 24px;
    box-shadow: 0 18px 42px rgba(16,32,51,.22);
    text-align: center !important;
}

.hero h1 {
    color: white;
    font-size: 2.2rem;
    margin: 0;
    font-weight: 900;
    letter-spacing: .2px;
    text-align: center !important;
}

div[data-testid="stFileUploader"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 22px !important;
    padding: 22px !important;
    margin: 0 auto 22px auto !important;
    box-shadow: 0 8px 22px rgba(16,32,51,.045) !important;
    text-align: center !important;
    direction: rtl !important;
}

div[data-testid="stFileUploader"] label {
    text-align: center !important;
    display: block !important;
    font-size: 1.15rem !important;
    font-weight: 900 !important;
    color: var(--text) !important;
    margin-bottom: 12px !important;
}

div[data-testid="stFileUploader"] section {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    direction: rtl !important;
    border: 1.5px dashed #c7d3e1 !important;
    border-radius: 18px !important;
    background: #f8fafc !important;
    padding: 28px !important;
}

div[data-testid="stFileUploader"] button {
    position: relative !important;
    background: var(--teal) !important;
    color: transparent !important;
    font-size: 0 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 10px 24px !important;
    margin: 12px auto !important;
    min-width: 185px !important;
    height: 46px !important;
    overflow: hidden !important;
}

div[data-testid="stFileUploader"] button::after {
    content: "יש לבחור קובץ להעלאה";
    color: white !important;
    font-size: 1rem !important;
    font-weight: 900 !important;
    position: absolute !important;
    inset: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    direction: rtl !important;
}

div[data-testid="stFileUploader"] small,
div[data-testid="stFileUploader"] span,
div[data-testid="stFileUploader"] p {
    text-align: center !important;
    direction: rtl !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--card) !important;
    border-color: var(--border) !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 20px rgba(16,32,51,.04);
    margin-bottom: 18px !important;
}

div[data-testid="stMetric"] {
    background: linear-gradient(135deg,#ffffff 0%,#f8fafc 100%);
    border: 1px solid var(--border);
    padding: 18px;
    border-radius: 20px;
    box-shadow: 0 8px 22px rgba(16,32,51,.055);
    min-height: 108px;
}

div[data-testid="stMetricLabel"] {
    color: var(--muted);
    font-weight: 800;
    text-align: right !important;
}

div[data-testid="stMetricValue"] {
    color: var(--text);
    font-size: 1.34rem;
    font-weight: 950;
    text-align: right !important;
}


.metric-lines {
    direction: rtl;
    text-align: right;
    color: var(--text);
    line-height: 1.55;
    font-weight: 950;
    font-size: 1.05rem;
    white-space: normal;
}
.metric-lines .metric-total {
    font-size: 1.12rem;
    margin-bottom: 4px;
}
.metric-lines .metric-years {
    display: flex;
    flex-wrap: wrap;
    gap: 6px 10px;
    font-size: .92rem;
    color: #334155;
}
.metric-lines .metric-year {
    background: #f8fafc;
    border: 1px solid #e1e7ef;
    border-radius: 999px;
    padding: 2px 8px;
}

.custom-metric-card {
    background: linear-gradient(135deg,#ffffff 0%,#f8fafc 100%);
    border: 1px solid var(--border);
    padding: 18px;
    border-radius: 20px;
    box-shadow: 0 8px 22px rgba(16,32,51,.055);
    min-height: 108px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.custom-metric-label {
    color: var(--muted);
    font-weight: 800;
    text-align: right !important;
    margin-bottom: 8px;
    font-size: .86rem;
}
.custom-metric-card .metric-lines {
    min-height: 54px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

div[data-testid="stSelectbox"],
div[data-testid="stMultiSelect"],
div[data-baseweb="select"] {
    direction: rtl !important;
    text-align: right !important;
}

/* תובנות קומפקטיות - לא קופסאות גדולות */
.insight-strip {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 14px 16px;
    margin: 10px 0 18px 0;
    box-shadow: 0 8px 20px rgba(16,32,51,.04);
}

.insight-title {
    font-size: 1.05rem;
    font-weight: 950;
    color: var(--text);
    margin-bottom: 10px;
}

.insight-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.insight-pill {
    display: inline-flex;
    align-items: center;
    padding: 7px 12px;
    border-radius: 999px;
    font-size: .88rem;
    font-weight: 850;
    border: 1px solid #dbe4ef;
    background: #f8fafc;
    color: #334155;
}

.insight-pill.good { background: var(--green-bg); color: var(--green); border-color: #bbf7d0; }
.insight-pill.warn { background: var(--amber-bg); color: var(--amber); border-color: #f8ddb0; }
.insight-pill.bad { background: var(--red-bg); color: var(--red); border-color: #ffd0cc; }

.chart-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 16px 18px 8px 18px;
    margin-bottom: 18px;
    box-shadow: 0 8px 22px rgba(16,32,51,.045);
}

.table-title {
    color: var(--text);
    font-size: 1.18rem;
    font-weight: 950;
    margin: 18px 0 10px 0;
}

.table-wrap {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 14px;
    margin-top: 8px;
    margin-bottom: 18px;
    box-shadow: 0 8px 22px rgba(16,32,51,.045);
    direction: rtl;
    text-align: right;
}

.table-scroll {
    overflow: auto;
    max-height: 430px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    direction: rtl;
}

table.prof-table {
    width: 100%;
    border-collapse: collapse;
    direction: rtl;
    text-align: right;
    font-size: .9rem;
    background: white;
}

table.prof-table thead th {
    position: sticky;
    top: 0;
    z-index: 3;
    background: var(--navy);
    color: white;
    padding: 11px 12px;
    border-bottom: 1px solid #334155;
    white-space: nowrap;
    font-weight: 900;
    text-align: right;
}

table.prof-table tbody td {
    padding: 10px 12px;
    border-bottom: 1px solid #e5e7eb;
    color: var(--text);
    white-space: nowrap;
    max-width: 310px;
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: right;
    direction: rtl;
}

table.prof-table tbody tr:nth-child(even) {
    background: #f8fafc;
}

table.prof-table tbody tr:hover {
    background: var(--blue-soft);
}

.table-caption {
    color: var(--muted);
    font-size: .86rem;
    margin: 4px 0 8px 0;
    text-align: right;
}

.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    font-weight: 900;
    font-size: .82rem;
    line-height: 1.4;
}

.badge-red {
    color: var(--red);
    background: var(--red-bg);
    border: 1px solid #ffd0cc;
}

.badge-yellow {
    color: var(--amber);
    background: var(--amber-bg);
    border: 1px solid #f8ddb0;
}

.badge-green {
    color: var(--green);
    background: var(--green-bg);
    border: 1px solid #bbf7d0;
}

.badge-purple {
    color: var(--purple);
    background: var(--purple-bg);
    border: 1px solid #ddd6fe;
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def norm(v):
    if pd.isna(v):
        return ""
    v = str(v)
    v = v.replace("\u200f", "").replace("\u200e", "")
    v = v.replace("–", "-").replace("—", "-").replace("−", "-")
    v = v.replace("״", '"').replace("׳", "'")
    return " ".join(v.split()).strip()


def normalize_columns(df):
    df = df.copy()
    df.columns = [norm(c) for c in df.columns]
    return df


def find_col(df, names):
    normalized = {norm(c): c for c in df.columns}
    for name in names:
        key = norm(name)
        if key in normalized:
            return normalized[key]
    return None



def find_col_fuzzy(df, includes, excludes=None):
    """
    זיהוי עמודה גם כשהכותרת לא זהה בדיוק אלא כוללת טקסט נוסף/רווחים/שורות.
    """
    excludes = excludes or []
    includes = [norm(x).lower() for x in includes]
    excludes = [norm(x).lower() for x in excludes]

    best_col = None
    best_score = -1

    for col in df.columns:
        c = norm(col).lower()
        if any(ex in c for ex in excludes):
            continue

        score = 0
        for inc in includes:
            if inc and inc in c:
                score += len(inc)

        if score > best_score and score > 0:
            best_score = score
            best_col = col

    return best_col


def smart_find_col(df, exact_names, includes=None, excludes=None):
    """
    קודם מחפש התאמה מדויקת, ואם אין — מחפש התאמה חלקית.
    """
    exact = find_col(df, exact_names)
    if exact:
        return exact
    return find_col_fuzzy(df, includes or exact_names, excludes or [])


def compact_key(v):
    s = clean_key(v).lower()
    for ch in [" ", "-", "_", "/", "\\", ".", ":", ";", "(", ")", "[", "]"]:
        s = s.replace(ch, "")
    return s.lstrip("0")


def key_variants(values):
    out = set()
    for v in values:
        a = clean_key(v)
        b = compact_key(v)
        if a:
            out.add(a)
        if b:
            out.add(b)
    return out


def series_matches_values(series, values):
    vals = key_variants(values)
    if not vals:
        return pd.Series(False, index=series.index)
    a = series.apply(clean_key).isin(vals)
    b = series.apply(compact_key).isin(vals)
    return a | b


def researcher_matches(series, researcher):
    target = norm(researcher).lower()
    target_compact = compact_key(researcher)
    if not target:
        return pd.Series(False, index=series.index)

    s_norm = series.astype(str).map(norm).str.lower()
    s_compact = series.astype(str).map(compact_key)

    return (
        (s_norm == target)
        | (s_norm.str.contains(target, regex=False, na=False))
        | (pd.Series([target in x for x in s_norm], index=series.index))
        | (s_compact == target_compact)
        | (s_compact.str.contains(target_compact, regex=False, na=False))
    )


def numeric_col_strength(df, col):
    if not col or col not in df.columns:
        return 0
    try:
        return float(to_num(df[col]).abs().sum())
    except Exception:
        return 0


def best_numeric_col(df, includes, excludes=None):
    candidates = []
    excludes = excludes or []
    for col in df.columns:
        c = norm(col).lower()
        if any(norm(ex).lower() in c for ex in excludes):
            continue
        if any(norm(inc).lower() in c for inc in includes):
            strength = numeric_col_strength(df, col)
            candidates.append((strength, col))
    candidates = sorted(candidates, reverse=True)
    if candidates and candidates[0][0] > 0:
        return candidates[0][1]
    return None


def improve_payment_columns(det_raw, D):
    """
    תיקון ספציפי לטאב מעקב הוצאות והכנסות:
    אם עמודות הכסף לא זוהו או שהעמודה שזוהתה מחזירה 0, מחפש עמודה אחרת לפי טקסט חלקי וסכום מספרי.
    """
    fixed = D.copy()

    rules = {
        "budget_total": (["תקציב"], ["יתרה", "ניצול", "אחוז", "%", "wbs", "מספר"]),
        "purchase_commitments": (["רכש", "התחייב"], ["יתרה", "ניצול", "אחוז", "%"]),
        "execution_total": (["ביצוע"], ["יתרה", "ניצול", "אחוז", "%"]),
        "balance": (["יתרה"], ["אחוז", "%"]),
    }

    for key, (includes, excludes) in rules.items():
        current = fixed.get(key)
        if (not current) or (current not in det_raw.columns) or numeric_col_strength(det_raw, current) == 0:
            candidate = best_numeric_col(det_raw, includes, excludes)
            if candidate:
                fixed[key] = candidate

    return fixed



def clean_key(v):
    if pd.isna(v):
        return ""
    s = str(v).strip()
    if s.lower() in ["nan", "none", "nat"]:
        return ""
    try:
        f = float(s)
        if f.is_integer():
            return str(int(f))
    except Exception:
        pass
    if s.endswith(".0") and s[:-2].replace("-", "").isdigit():
        return s[:-2]
    return norm(s)


def to_num(s):
    if s is None:
        return pd.Series(dtype="float64")
    x = s.astype(str).str.strip()
    neg = x.str.match(r"^\(.*\)$", na=False)
    x = (
        x.str.replace(",", "", regex=False)
        .str.replace("₪", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace("€", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.replace("\u200f", "", regex=False)
        .str.replace("\u200e", "", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.strip()
        .replace({"": np.nan, "nan": np.nan, "None": np.nan, "NaT": np.nan, "-": np.nan})
    )
    out = pd.to_numeric(x, errors="coerce").fillna(0)
    out[neg] = -out[neg]
    return out


def make_numeric(df, cols):
    df = df.copy()
    for c in cols:
        if c and c in df.columns:
            df[c] = to_num(df[c])
    return df


def money(v):
    try:
        return f"{float(v):,.0f} ₪"
    except Exception:
        return "0 ₪"


def number(v):
    try:
        return f"{float(v):,.0f}"
    except Exception:
        return "0"


def pct(v):
    try:
        return f"{float(v):,.1f}%"
    except Exception:
        return "0%"


def compact(v):
    try:
        v = float(v)
    except Exception:
        return "0"
    if abs(v) >= 1_000_000:
        return f"{v / 1_000_000:.1f}M"
    if abs(v) >= 1_000:
        return f"{v / 1_000:.0f}K"
    return f"{v:,.0f}"


def sum_col(df, col):
    if df is not None and col and col in df.columns:
        return to_num(df[col]).sum()
    return 0


def count_studies(df, uniq=None, study_id=None):
    if df is None or df.empty:
        return 0
    if uniq and uniq in df.columns:
        val = to_num(df[uniq]).sum()
        if val > 0:
            return val
    if study_id and study_id in df.columns:
        return df[study_id].dropna().apply(clean_key).replace("", np.nan).dropna().nunique()
    return len(df)


def budget_status(v):
    try:
        v = float(v)
    except Exception:
        return "לא ידוע"
    if v < 20:
        return "ניצול נמוך"
    if v <= 80:
        return "תקין"
    if v <= 100:
        return "קרוב לניצול מלא"
    return "חריגה"


def recruitment_status(v):
    try:
        v = float(v)
    except Exception:
        return "לא ידוע"
    if v == 0:
        return "אין גיוס"
    if v < 50:
        return "גיוס נמוך"
    if v < 80:
        return "גיוס בינוני"
    return "גיוס תקין"


def traffic_light(status, balance=None, days=None, recruit=None):
    if status == "חריגה":
        return "🔴 אדום"
    try:
        if balance is not None and float(balance) < 0:
            return "🔴 אדום"
    except Exception:
        pass
    try:
        if days is not None and 0 <= float(days) <= 60:
            return "🟡 צהוב"
    except Exception:
        pass
    try:
        if recruit is not None and float(recruit) < 50:
            return "🟡 צהוב"
    except Exception:
        pass
    if status in ["ניצול נמוך", "קרוב לניצול מלא", "לא ידוע"]:
        return "🟡 צהוב"
    return "🟢 ירוק"


def funding_group(v):
    t = norm(v).lower()
    if any(w in t for w in ["גרנט", "grant", "מענק", "קרן", "foundation"]):
        return "גרנט"
    if any(w in t for w in ["יזם", "industry", "commercial", "חברה", "תעשייה", "מסחרי"]):
        return "מחקר יזם"
    if not t:
        return "לא סווג"
    return "אחר"


def add_realization(df, expected, actual):
    df = df.copy()
    if expected and actual and expected in df.columns and actual in df.columns:
        e = to_num(df[expected])
        a = to_num(df[actual])
        df["שיעור מימוש הכנסות"] = np.where(e > 0, a / e * 100, 0)
    else:
        df["שיעור מימוש הכנסות"] = 0
    return df


def safe_display(v):
    if pd.isna(v):
        return ""
    s = str(v).strip()
    if s.lower() in ["nan", "none", "nat"]:
        return ""
    if s.endswith(".0") and s[:-2].replace("-", "").isdigit():
        return s[:-2]
    return s


def badge_html(v):
    text = safe_display(v)
    if "🔴" in text or "חריגה" in text or "אדום" in text:
        cls = "badge-red"
    elif "🟡" in text or "צהוב" in text or "ניצול נמוך" in text or "קרוב" in text or "גיוס נמוך" in text or "אין גיוס" in text:
        cls = "badge-yellow"
    elif "🟢" in text or "ירוק" in text or "תקין" in text:
        cls = "badge-green"
    elif text in ["מחקר יזם", "גרנט", "אחר", "לא סווג"]:
        cls = "badge-purple"
    else:
        cls = ""
    if cls:
        return f'<span class="badge {cls}">{escape(text)}</span>'
    return escape(text)


def format_html_cell(value, col, money_cols=None, pct_cols=None, num_cols=None, date_cols=None):
    money_cols = money_cols or []
    pct_cols = pct_cols or []
    num_cols = num_cols or []
    date_cols = date_cols or []
    if col in money_cols:
        return escape(money(value))
    if col in pct_cols:
        return escape(pct(value))
    if col in num_cols:
        return escape(number(value))
    if col in date_cols:
        dt = pd.to_datetime(value, errors="coerce")
        if pd.isna(dt):
            return ""
        return escape(dt.strftime("%d/%m/%Y"))
    if col in ["סטטוס ניצול תקציב - מחושב", "סטטוס גיוס", "רמזור ניהולי", "קבוצת מימון"]:
        return badge_html(value)
    return escape(safe_display(value))


def render_table(df, title, cols=None, money_cols=None, pct_cols=None, num_cols=None, date_cols=None, height=430, max_rows=180):
    st.markdown(f'<div class="table-title">{escape(str(title))}</div>', unsafe_allow_html=True)
    if df is None or df.empty:
        st.info("אין נתונים להצגה בהתאם לבחירה הנוכחית.")
        return
    data = df.copy()
    if cols:
        cols = [c for c in cols if c and c in data.columns]
        if cols:
            data = data[cols]
    if data.empty:
        st.info("אין נתונים להצגה בהתאם לבחירה הנוכחית.")
        return
    total_rows = len(data)
    if total_rows > max_rows:
        shown = data.head(max_rows)
        caption = f"מוצגות {max_rows:,} שורות מתוך {total_rows:,}. ניתן להוריד את הדוח המלא לאקסל."
    else:
        shown = data
        caption = f"מוצגות {total_rows:,} שורות."
    headers = "".join(f"<th>{escape(str(c))}</th>" for c in shown.columns)
    rows = []
    for _, row in shown.iterrows():
        cells = []
        for c in shown.columns:
            title_value = escape(safe_display(row[c]), quote=True)
            cell_value = format_html_cell(row[c], c, money_cols, pct_cols, num_cols, date_cols)
            cells.append(f"<td title='{title_value}'>{cell_value}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    html = f"""
    <div class="table-wrap">
        <div class="table-caption">{escape(caption)}</div>
        <div class="table-scroll" style="max-height:{int(height)}px;">
            <table class="prof-table">
                <thead><tr>{headers}</tr></thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def kpis(items, columns_per_row=4):
    if not items:
        return

    for start in range(0, len(items), columns_per_row):
        chunk = items[start:start + columns_per_row]
        cols = st.columns(len(chunk))

        for c, (label, value) in zip(cols, chunk):
            with c:
                with st.container(border=True):
                    if isinstance(value, str) and value.strip().startswith("<div class=\"metric-lines\""):
                        st.markdown(
                            f'''
                            <div class="custom-metric-card">
                                <div class="custom-metric-label">{escape(str(label))}</div>
                                {value}
                            </div>
                            ''',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.metric(label, value)


def chart_start():
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)


def chart_end():
    st.markdown("</div>", unsafe_allow_html=True)


def base(fig, h=400):
    fig.update_layout(
        height=h,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(size=13, color="#334155", family="Calibri, Arial, sans-serif"),
        title=dict(x=.5, font=dict(size=18, color="#111827")),
        margin=dict(l=40, r=40, t=80, b=60),
        legend=dict(title=""),
    )
    return fig


def bar(df, x, y, title, h=390, color="#245c9f"):
    if df is None or df.empty or x not in df.columns or y not in df.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return
    d = df.copy()
    d[x] = d[x].astype(str)
    d["תווית"] = d[y].apply(compact)
    fig = px.bar(d, x=x, y=y, text="תווית", title=title)
    fig.update_traces(textposition="outside", cliponaxis=False, marker_color=color)
    fig.update_layout(xaxis=dict(type="category"), yaxis=dict(gridcolor="#e2e8f0"), bargap=.38)
    st.plotly_chart(base(fig, h), use_container_width=True)


def grouped(df, x, ycols, title, h=430):
    if df is None or df.empty:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return
    ycols = [c for c in ycols if c and c in df.columns]
    if not ycols or x not in df.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return
    m = df.melt(id_vars=[x], value_vars=ycols, var_name="מדד", value_name="ערך")
    m["תווית"] = m["ערך"].apply(compact)
    fig = px.bar(
        m, x=x, y="ערך", color="מדד", barmode="group", text="תווית", title=title,
        color_discrete_sequence=["#245c9f", "#167c80", "#8a6f2a", "#7c3aed", "#475569"],
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(xaxis=dict(type="category"), yaxis=dict(gridcolor="#e2e8f0"), bargap=.34)
    st.plotly_chart(base(fig, h), use_container_width=True)


def donut(df, names, values, title, h=380):
    if df is None or df.empty or names not in df.columns or values not in df.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return
    fig = px.pie(
        df, names=names, values=values, hole=.54, title=title,
        color_discrete_sequence=["#245c9f", "#167c80", "#8a6f2a", "#6b7280", "#b7791f", "#5b4b8a", "#0f5f63"],
    )
    # מציג בתוך הפאי גם מספר וגם אחוז
    fig.update_traces(
        textposition="inside",
        texttemplate="%{label}<br>%{value:,.0f} (%{percent})",
        hovertemplate="%{label}<br>מספר: %{value:,.0f}<br>אחוז: %{percent}<extra></extra>",
    )
    st.plotly_chart(base(fig, h), use_container_width=True)


def top10(df, label, value, title):
    if df is None or df.empty or label not in df.columns or value not in df.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return
    d = df.sort_values(value).tail(10).copy()
    d["שם מקוצר"] = d[label].astype(str).apply(lambda s: s[:25] + "..." if len(s) > 28 else s)
    d["תווית"] = d[value].apply(compact)
    fig = px.bar(d, x=value, y="שם מקוצר", orientation="h", text="תווית", title=title, hover_data={label: True})
    fig.update_traces(textposition="outside", cliponaxis=False, marker_color="#245c9f")
    fig.update_layout(yaxis=dict(title=""), xaxis=dict(gridcolor="#e2e8f0"), showlegend=False)
    st.plotly_chart(base(fig, max(420, len(d) * 48 + 140)), use_container_width=True)


def explain():
    with st.expander("הסבר קצר על המדדים", expanded=False):
        st.markdown(
            """
            <div style="direction:rtl;text-align:right;line-height:1.8">
            <b>מימוש הכנסות</b> = הכנסות בפועל חלקי צפי הכנסות.<br>
            <b>ניצול תקציב</b> = סה״כ ניצול חלקי תקציב.<br>
            <b>סטטוס גיוס</b> = משתתפים בפועל חלקי צפי משתתפים.
            </div>
            """,
            unsafe_allow_html=True,
        )


def insights(data, C):
    if data is None or data.empty:
        return [("אין נתונים", "warn")]

    total = count_studies(data, C.get("unique_study"), C.get("study_id"))
    exp = sum_col(data, C.get("expected_income"))
    act = sum_col(data, C.get("actual_income"))
    exps = sum_col(data, C.get("total_expenses"))

    items = [("מחקרים: " + number(total), "good")]

    if exp > 0:
        real = act / exp * 100
        items.append(("מימוש הכנסות: " + pct(real), "good" if real >= 80 else "warn" if real >= 50 else "bad"))

    if act > 0 and exps > 0:
        er = exps / act * 100
        items.append(("הוצאות מתוך הכנסות: " + pct(er), "bad" if er > 90 else "warn" if er > 70 else "good"))

    if "סטטוס ניצול תקציב - מחושב" in data.columns:
        n = len(data[data["סטטוס ניצול תקציב - מחושב"] == "חריגה"])
        if n > 0:
            items.append(("חריגות תקציב: " + number(n), "bad"))

    if "סטטוס גיוס" in data.columns:
        n = len(data[data["סטטוס גיוס"].isin(["אין גיוס", "גיוס נמוך"])])
        if n > 0:
            items.append(("גיוס נמוך/אין גיוס: " + number(n), "warn"))

    return items[:5]


def render_insights(title, items):
    if not items:
        return
    pills = []
    for txt, kind in items:
        icon = "●"
        cls = "good" if kind == "good" else "warn" if kind == "warn" else "bad"
        pills.append(f'<span class="insight-pill {cls}">{icon} {escape(str(txt))}</span>')
    st.markdown(
        f"""
        <div class="insight-strip">
            <div class="insight-title">{escape(str(title))}</div>
            <div class="insight-row">{''.join(pills)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_identity_cards(cards):
    for start in range(0, len(cards), 4):
        row_cards = cards[start:start + 4]
        cols = st.columns(len(row_cards))

        for col, (label, value) in zip(cols, row_cards):
            with col:
                with st.container(border=True):
                    st.caption(str(label))
                    st.markdown(f"**{safe_display(value)}**")


def filter_select(df, label, col, key):
    if not col or col not in df.columns:
        return df, None
    vals = sorted([v for v in df[col].dropna().astype(str).unique() if norm(v)])
    if not vals:
        return df.iloc[0:0], None
    sel = st.selectbox(label, vals, key=key)
    return df[df[col].astype(str) == sel], sel


def filter_multi(df, label, col, key, default_all=False):
    if not col or col not in df.columns:
        return df
    vals = sorted([v for v in df[col].dropna().astype(str).unique() if norm(v)])
    if not vals:
        return df.iloc[0:0]
    selected = st.multiselect(
        label, vals, default=vals if default_all else [],
        key=key, placeholder="בחירה אופציונלית לסינון",
    )
    if selected:
        return df[df[col].astype(str).isin(selected)]
    return df


def read_excel_smart(xls, sheet_name):
    """
    קורא גיליון גם כאשר הכותרות לא נמצאות בשורה הראשונה.
    שומר על studies_data כרגיל, אבל מציל בעיקר את גיליון פירוט הוצאות והכנסות.
    """
    preview = pd.read_excel(xls, sheet_name=sheet_name, header=None, nrows=25)
    header_keywords = [
        "מספר הלסינקי", "study_id", "סוג תכנית-study_id", "מספר פרוטוקול",
        "שם חוקר ראשי", "חוקר ראשי", "קטגוריית סעיף תקציבי",
        "סהכ תקציב", "סה\"כ תקציב", "התחייבויות רכש",
        "סהכ ביצוע", "סה\"כ ביצוע", "יתרה לניצול", "אלמנט WBS"
    ]

    best_row = 0
    best_score = -1

    for i in range(len(preview)):
        row_values = [norm(v).lower() for v in preview.iloc[i].tolist()]
        score = 0
        for cell in row_values:
            for kw in header_keywords:
                if norm(kw).lower() in cell:
                    score += 1
        if score > best_score:
            best_score = score
            best_row = i

    return normalize_columns(pd.read_excel(xls, sheet_name=sheet_name, header=best_row))


def study_count_by_year_text(data, C):
    total = count_studies(data, C.get("unique_study"), C.get("study_id"))

    if not C.get("approval_year") or C["approval_year"] not in data.columns:
        return (
            f'<div class="metric-lines">'
            f'<div class="metric-total">סה״כ: {number(total)}</div>'
            f'</div>'
        )

    if C.get("unique_study") and C["unique_study"] in data.columns:
        s = data.groupby(C["approval_year"])[C["unique_study"]].sum()
    elif C.get("study_id") and C["study_id"] in data.columns:
        temp = data[[C["approval_year"], C["study_id"]]].copy()
        temp["__id__"] = temp[C["study_id"]].apply(clean_key)
        temp = temp[temp["__id__"] != ""]
        s = temp.groupby(C["approval_year"])["__id__"].nunique()
    else:
        s = data.groupby(C["approval_year"]).size()

    year_items = []
    for year, val in s.sort_index().items():
        year_items.append(
            f'<span class="metric-year">{escape(safe_display(year))}: {number(val)}</span>'
        )

    return (
        f'<div class="metric-lines">'
        f'<div class="metric-total">סה״כ: {number(total)}</div>'
        f'<div class="metric-years">{"".join(year_items)}</div>'
        f'</div>'
    )
def study_count_summary_df(data, C):
    if data is None or data.empty or not C.get("approval_year") or C["approval_year"] not in data.columns:
        return pd.DataFrame(columns=["שנה", "קבוצת מימון", "מספר מחקרים", "אחוז"])

    if C.get("unique_study") and C["unique_study"] in data.columns:
        s = (
            data.groupby([C["approval_year"], "קבוצת מימון"], as_index=False)[C["unique_study"]]
            .sum()
            .rename(columns={C["approval_year"]: "שנה", C["unique_study"]: "מספר מחקרים"})
        )
    elif C.get("study_id") and C["study_id"] in data.columns:
        temp = data[[C["approval_year"], "קבוצת מימון", C["study_id"]]].copy()
        temp["__id__"] = temp[C["study_id"]].apply(clean_key)
        temp = temp[temp["__id__"] != ""]
        s = (
            temp.groupby([C["approval_year"], "קבוצת מימון"], as_index=False)["__id__"]
            .nunique()
            .rename(columns={C["approval_year"]: "שנה", "__id__": "מספר מחקרים"})
        )
    else:
        s = data.groupby([C["approval_year"], "קבוצת מימון"], as_index=False).size().rename(
            columns={C["approval_year"]: "שנה", "size": "מספר מחקרים"}
        )

    s["סה״כ שנה"] = s.groupby("שנה")["מספר מחקרים"].transform("sum")
    s["אחוז"] = np.where(s["סה״כ שנה"] > 0, s["מספר מחקרים"] / s["סה״כ שנה"] * 100, 0)
    s["תווית"] = s.apply(lambda r: f'{number(r["מספר מחקרים"])} ({r["אחוז"]:.1f}%)', axis=1)
    s["שנה"] = s["שנה"].astype(str)
    return s


def studies_by_year_funding_bar(data, C, title):
    s = study_count_summary_df(data, C)
    if s.empty:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    # גרף עמודות מקובצות ולא stacked, כדי שגם מספרים קטנים יהיו קריאים יותר.
    max_y = max(float(s["מספר מחקרים"].max()), 1)
    fig = px.bar(
        s,
        x="שנה",
        y="מספר מחקרים",
        color="קבוצת מימון",
        text="תווית",
        title=title,
        barmode="group",
        color_discrete_sequence=["#245c9f", "#167c80", "#8a6f2a", "#6b7280", "#b7791f"],
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        xaxis=dict(type="category"),
        yaxis=dict(gridcolor="#e2e8f0", range=[0, max_y * 1.22]),
        bargap=.28,
        bargroupgap=.08,
        uniformtext_minsize=10,
        uniformtext_mode="show",
    )
    st.plotly_chart(base(fig, 430), use_container_width=True)


def expected_actual_by_year_chart(data, C, title):
    year = C.get("approval_year")
    expected = C.get("expected_income")
    actual = C.get("actual_income")
    if not year or not expected or not actual or year not in data.columns or expected not in data.columns or actual not in data.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    s = (
        data.groupby(year, as_index=False)[[expected, actual]]
        .sum()
        .rename(columns={year: "שנה", expected: "צפי הכנסות", actual: "הכנסות בפועל"})
    )
    s["שנה"] = s["שנה"].astype(str)
    s["אחוז מימוש"] = np.where(s["צפי הכנסות"] > 0, s["הכנסות בפועל"] / s["צפי הכנסות"] * 100, 0)

    m = s.melt(
        id_vars=["שנה", "אחוז מימוש"],
        value_vars=["צפי הכנסות", "הכנסות בפועל"],
        var_name="מדד",
        value_name="סכום",
    )
    m["תווית"] = m.apply(
        lambda r: f'{compact(r["סכום"])}' if r["מדד"] == "צפי הכנסות" else f'{compact(r["סכום"])} ({r["אחוז מימוש"]:.1f}%)',
        axis=1,
    )

    fig = px.bar(
        m,
        x="שנה",
        y="סכום",
        color="מדד",
        barmode="group",
        text="תווית",
        title=title,
        color_discrete_sequence=["#245c9f", "#167c80"],
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(xaxis=dict(type="category"), yaxis=dict(gridcolor="#e2e8f0"), bargap=.34)
    st.plotly_chart(base(fig, 410), use_container_width=True)


def expense_stacked_by_year_chart(data, C, expense_map, title):
    year = C.get("approval_year")
    if not year or year not in data.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    items = []
    for exp_name, col in expense_map.items():
        if col and col in data.columns:
            temp = data.groupby(year, as_index=False)[col].sum().rename(columns={year: "שנה", col: "סכום"})
            temp["סוג הוצאה"] = exp_name
            items.append(temp)

    if not items:
        st.info("אין הוצאות להצגה בהתאם לסינון הנוכחי.")
        return

    s = pd.concat(items, ignore_index=True)
    s = s[s["סכום"] != 0]
    if s.empty:
        st.info("אין הוצאות להצגה בהתאם לסינון הנוכחי.")
        return

    s["שנה"] = s["שנה"].astype(str)
    s["תווית"] = s["סכום"].apply(compact)

    fig = px.bar(
        s,
        x="שנה",
        y="סכום",
        color="סוג הוצאה",
        text="תווית",
        title=title,
        barmode="stack",
        color_discrete_sequence=["#245c9f", "#167c80", "#8a6f2a", "#6b7280", "#b7791f"],
    )
    fig.update_traces(textposition="inside", cliponaxis=False)
    fig.update_layout(xaxis=dict(type="category"), yaxis=dict(gridcolor="#e2e8f0"), bargap=.34)
    st.plotly_chart(base(fig, 410), use_container_width=True)


def get_department_from_source(details, source, C, D):
    if details is None or details.empty or not C.get("department") or C["department"] not in source.columns:
        return details
    if D.get("study_id") and D["study_id"] in details.columns and C.get("study_id") and C["study_id"] in source.columns:
        ids = set(source[C["study_id"]].dropna().apply(clean_key))
        ids.discard("")
        if ids:
            return details[details[D["study_id"]].apply(clean_key).isin(ids)]
    if D.get("protocol") and D["protocol"] in details.columns and C.get("protocol") and C["protocol"] in source.columns:
        ps = set(source[C["protocol"]].dropna().apply(clean_key))
        ps.discard("")
        if ps:
            return details[details[D["protocol"]].apply(clean_key).isin(ps)]
    return details



def choose_details_sheet(xls, studies_sheet):
    """
    תיקון קריטי:
    בחירת גיליון פירוט הוצאות והכנסות פר מחקר לפי שם הגיליון וגם לפי עמודות בפועל.
    """
    preferred_names = [
        "פירוט הוצאות והכנסות פר מחקר",
        "פירוט הווצאות והכנסות פר מחקר",
        "מעקב הוצאות והכנסות",
        "פירוט הוצאות והכנסות",
        "דרישות תשלום",
        "מעקב דרישות תשלום",
    ]

    sheet_names_norm = {norm(s).lower(): s for s in xls.sheet_names}

    for name in preferred_names:
        key = norm(name).lower()
        if key in sheet_names_norm:
            return sheet_names_norm[key]

    best_sheet = None
    best_score = -1

    for s in xls.sheet_names:
        if s == studies_sheet:
            continue
        try:
            sample = read_excel_smart(xls, s).head(20)
        except Exception:
            continue

        score = 0
        checks = [
            find_col(sample, ["קטגוריית סעיף תקציבי"]),
            find_col(sample, ["מספר הלסינקי", "study_id", "סוג תכנית-study_id"]),
            find_col(sample, ["מספר פרוטוקול", "סימון פרוטוקול"]),
            find_col(sample, ["סה\"כ ביצוע", "סהכ ביצוע"]),
            find_col(sample, ["סה\"כ תקציב מ", "סהכ תקציב מ"]),
            find_col(sample, ["התחייבויות רכש"]),
            find_col(sample, ["יתרה לניצול"]),
            find_col(sample, ["אלמנט WBS", "מספר WBS"]),
        ]
        score = sum(x is not None for x in checks)

        if score > best_score:
            best_score = score
            best_sheet = s

    return best_sheet or studies_sheet


def payment_for(details, source, C, D, researcher=None):
    """
    מחבר בין studies_data לבין גיליון פירוט הוצאות והכנסות פר מחקר.
    החיבור נעשה בצורה גמישה לפי מספר הלסינקי / פרוטוקול / WBS / חוקר.
    """
    if details is None or details.empty:
        return pd.DataFrame()

    d = details.copy()
    masks = []

    if C.get("study_id") and D.get("study_id") and C["study_id"] in source.columns and D["study_id"] in d.columns:
        ids = list(source[C["study_id"]].dropna())
        mask = series_matches_values(d[D["study_id"]], ids)
        if mask.any():
            masks.append(mask)

    if C.get("protocol") and D.get("protocol") and C["protocol"] in source.columns and D["protocol"] in d.columns:
        ps = list(source[C["protocol"]].dropna())
        mask = series_matches_values(d[D["protocol"]], ps)
        if mask.any():
            masks.append(mask)

    if C.get("wbs") and D.get("wbs") and C["wbs"] in source.columns and D["wbs"] in d.columns:
        ws = list(source[C["wbs"]].dropna())
        mask = series_matches_values(d[D["wbs"]], ws)
        if mask.any():
            masks.append(mask)

    if researcher and D.get("pi_name") and D["pi_name"] in d.columns:
        mask = researcher_matches(d[D["pi_name"]], researcher)
        if mask.any():
            masks.append(mask)

    if masks:
        m = masks[0]
        for x in masks[1:]:
            m = m | x
        d = d[m]

    return d



def value_from_single_row(source, col):
    """מחזיר ערך אחד מתוך שורת/שורות המחקר שנבחרו, אם קיים."""
    if source is None or source.empty or not col or col not in source.columns:
        return ""
    vals = [safe_display(v) for v in source[col].dropna().tolist() if safe_display(v)]
    return vals[0] if vals else ""


def ensure_payment_display_columns(pay, source, C, D):
    """
    מסדר את טבלת פירוט הוצאות והכנסות בלי לשנות את מקור הנתונים:
    מוסיף עמודות תצוגה קבועות למספר הלסינקי/פרוטוקול/WBS גם אם בגיליון הפירוט הן חסרות או ריקות.
    """
    if pay is None or pay.empty:
        return pay

    out = pay.copy()

    study_val = value_from_single_row(source, C.get("study_id"))
    protocol_val = value_from_single_row(source, C.get("protocol"))
    wbs_val = value_from_single_row(source, C.get("wbs"))

    if D.get("study_id") and D["study_id"] in out.columns:
        out["מספר הלסינקי"] = out[D["study_id"]].apply(safe_display)
        if study_val:
            out["מספר הלסינקי"] = out["מספר הלסינקי"].replace("", study_val)
    else:
        out["מספר הלסינקי"] = study_val

    if D.get("protocol") and D["protocol"] in out.columns:
        out["מספר פרוטוקול"] = out[D["protocol"]].apply(safe_display)
        if protocol_val:
            out["מספר פרוטוקול"] = out["מספר פרוטוקול"].replace("", protocol_val)
    else:
        out["מספר פרוטוקול"] = protocol_val

    if D.get("wbs") and D["wbs"] in out.columns:
        out["אלמנט WBS"] = out[D["wbs"]].apply(safe_display)
        if wbs_val:
            out["אלמנט WBS"] = out["אלמנט WBS"].replace("", wbs_val)
    else:
        out["אלמנט WBS"] = wbs_val

    return out


def clean_payment_columns(D):
    """עמודות נקיות לטבלאות פירוט הוצאות והכנסות, ללא שם חוקר וקבוצות התחייבות."""
    return [
        "מספר הלסינקי",
        "מספר פרוטוקול",
        "אלמנט WBS",
        D.get("site"),
        D.get("budget_category"),
        D.get("description"),
        D.get("budget_total"),
        D.get("purchase_commitments"),
        D.get("execution_total"),
        D.get("balance"),
    ]


def plot_realization_year(data, year, expected, actual):
    if not year or not expected or not actual:
        return
    if year not in data.columns or expected not in data.columns or actual not in data.columns:
        return
    s = (
        data.groupby(year, as_index=False)[[expected, actual]]
        .sum()
        .rename(columns={year: "שנה", expected: "צפי הכנסות", actual: "הכנסות בפועל"})
    )
    s["שיעור מימוש הכנסות"] = np.where(s["צפי הכנסות"] > 0, s["הכנסות בפועל"] / s["צפי הכנסות"] * 100, 0)
    s["תווית"] = s["שיעור מימוש הכנסות"].apply(lambda x: f"{x:.1f}%")
    fig = px.bar(s, x="שנה", y="שיעור מימוש הכנסות", text="תווית", title="שיעור מימוש הכנסות בפועל מתוך צפי לפי שנה")
    fig.update_traces(textposition="outside", cliponaxis=False, marker_color="#167c80")
    fig.update_layout(yaxis=dict(title="% מימוש", gridcolor="#e2e8f0"), xaxis=dict(type="category"))
    st.plotly_chart(base(fig, 390), use_container_width=True)


def funding_chart(data, uniq):
    if "קבוצת מימון" not in data.columns:
        return
    if uniq and uniq in data.columns:
        s = data.groupby("קבוצת מימון", as_index=False)[uniq].sum().rename(columns={uniq: "מספר מחקרים"})
    else:
        s = data.groupby("קבוצת מימון", as_index=False).size().rename(columns={"size": "מספר מחקרים"})
    donut(s, "קבוצת מימון", "מספר מחקרים", "התפלגות מחקרים לפי קבוצת מימון")


def expense_chart(data, expense_map, title):
    items = []
    for name, col in expense_map.items():
        if col and col in data.columns:
            val = sum_col(data, col)
            if val > 0:
                items.append((name, val))
    if not items:
        st.info("אין הוצאות להצגה בהתאם לסינון הנוכחי.")
        return
    s = pd.DataFrame(items, columns=["סוג הוצאה", "סכום"])
    donut(s, "סוג הוצאה", "סכום", title)


def budget_exec_chart(pay, D):
    items = []
    for name, key in [
        ("תקציב", "budget_total"),
        ("התחייבויות רכש", "purchase_commitments"),
        ("ביצוע", "execution_total"),
        ("יתרה לניצול", "balance"),
    ]:
        col = D.get(key)
        if col and col in pay.columns:
            items.append((name, sum_col(pay, col)))
    if not items:
        st.info("לא נמצאו נתוני תקציב / התחייבויות / ביצוע להצגה.")
        return
    s = pd.DataFrame(items, columns=["מדד", "סכום"])
    s = s[s["סכום"] != 0]
    if s.empty:
        st.info("אין נתונים תקציביים להצגה.")
        return
    s["תווית"] = s["סכום"].apply(compact)
    fig = px.bar(
        s, x="מדד", y="סכום", text="תווית", title="תקציב מול התחייבויות רכש, ביצוע ויתרה",
        color="מדד", color_discrete_sequence=["#245c9f", "#8a6f2a", "#b42318", "#167c80"],
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(showlegend=False, yaxis=dict(gridcolor="#e2e8f0"))
    st.plotly_chart(base(fig, 390), use_container_width=True)


def download_excel(df_to_download, file_name):
    if df_to_download is None or df_to_download.empty:
        return
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_to_download.to_excel(writer, index=False, sheet_name="data")
    st.download_button(
        "⬇️ הורדת הטבלה לאקסל",
        data=output.getvalue(),
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


# ============================================================
# NAVIGATION
# ============================================================

with st.sidebar:
    page = st.radio(
        "ניווט",
        [
            "כלל בית החולים",
            "מחלקות",
            "חוקרים",
            "יזמים",
            "סטטוס תקציב וגיוס",
            "דוח חוקר",
            "מעקב הוצאות והכנסות",
        ],
        label_visibility="collapsed",
    )

st.markdown(
    """
    <div class="hero">
        <h1>דשבורד ניהולי למחקרים קליניים</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# FILE UPLOAD
# ============================================================

if "uploaded_excel_file" not in st.session_state:
    st.session_state.uploaded_excel_file = None
if "uploaded_excel_name" not in st.session_state:
    st.session_state.uploaded_excel_name = None

upload_area = st.empty()

if st.session_state.uploaded_excel_file is None:
    with upload_area.container():
        uploaded_file = st.file_uploader("העלאת קובץ Excel", type=["xlsx"], label_visibility="visible")
    if uploaded_file is None:
        st.info("נא להעלות קובץ Excel כדי להציג את הדשבורד.")
        st.stop()
    st.session_state.uploaded_excel_file = uploaded_file.getvalue()
    st.session_state.uploaded_excel_name = uploaded_file.name
    upload_area.empty()
    st.rerun()

uploaded_file = BytesIO(st.session_state.uploaded_excel_file)

st.success(f"הקובץ נטען בהצלחה: {st.session_state.uploaded_excel_name}")

# ============================================================
# READ EXCEL
# ============================================================

try:
    xls = pd.ExcelFile(uploaded_file)

    studies_sheet = next((s for s in xls.sheet_names if norm(s).lower() == "studies_data"), xls.sheet_names[0])
    details_sheet = choose_details_sheet(xls, studies_sheet)

    raw = normalize_columns(pd.read_excel(xls, sheet_name=studies_sheet))
    det_raw = read_excel_smart(xls, details_sheet)

except Exception as e:
    st.error("לא אותר קובץ אקסל תקין. יש לנסות שוב.")
    st.exception(e)
    st.stop()

# ============================================================
# COLUMN MAPPING
# ============================================================

C = {
    "approval_date": find_col(raw, ["תאריך אישור מחקר"]),
    "approval_year": find_col(raw, ["שנת אישור המחקר", "שנת אישור מחקר"]),
    "start_date": find_col(raw, ["תאריך תחילה"]),
    "end_date": find_col(raw, ["תאריך סיום"]),
    "protocol": find_col(raw, ["סימון פרוטוקול", "מספר פרוטוקול"]),
    "study_id": find_col(raw, ["study_id", "סוג תכנית-study_id", "סוג תכנית – study_id", "סוג תכנית - study_id", "מספר הלסינקי"]),
    "pi": find_col(raw, ["חוקר ראשי", "שם חוקר ראשי"]),
    "site": find_col(raw, ["site", "SITE"]),
    "department": find_col(raw, ["מחלקה"]),
    "study_type": find_col(raw, ["סוג המחקר"]),
    "phase": find_col(raw, ["פאזת המחקר", "פאזה"]),
    "sponsor": find_col(raw, ["יזם", "גורם מממן"]),
    "funding_type": find_col(raw, ["סוג מימון"]),
    "expected_income": find_col(raw, ["צפי הכנסות (₪)", "צפי הכנסות ₪", "צפי הכנסות"]),
    "actual_income": find_col(raw, ["הכנסות בפועל"]),
    "total_expenses": find_col(raw, ["סך ההוצאות", "סה\"כ הוצאות", "סהכ הוצאות"]),
    "salary_expenses": find_col(raw, ["הוצאות- שכר", "הוצאות - שכר"]),
    "materials_expenses": find_col(raw, ["הוצאות- מתכלים", "הוצאות - מתכלים"]),
    "fixed_expenses": find_col(raw, ["הוצאות- קבוע", "הוצאות - קבוע"]),
    "travel_expenses": find_col(raw, ["הוצאות- נסיעות", "הוצאות - נסיעות"]),
    "internal_expenses": find_col(raw, ["הוצאות- העברות פנימיות", "הוצאות - העברות פנימיות"]),
    "expected_participants": find_col(raw, ["צפי משתתפים"]),
    "actual_participants": find_col(raw, ["משתתפים בפועל"]),
    "unique_study": find_col(raw, ["unique_study"]),
    "unique_researcher": find_col(raw, ["unique_researcher"]),
    "contract": find_col(raw, ["מספר מרכבה- מספר חוזה", "מספר מרכבה - מספר חוזה", "מספר חוזה"]),
    "budget_name": find_col(raw, ["שם תקציב"]),
    "budget_owner": find_col(raw, ["עובד אחראי- שם בעל התקציב", "עובד אחראי - שם בעל התקציב", "שם בעל התקציב"]),
    "wbs": find_col(raw, ["אלמנט WBS", "מספר WBS"]),
    "budget": find_col(raw, ["תקציב"]),
    "overhead": find_col(raw, ["תקורה לפי 18%", "תקורה"]),
    "commitment": find_col(raw, ["התחייבות", "התחייבויות"]),
    "execution": find_col(raw, ["ביצוע"]),
    "utilization_total": find_col(raw, ["סה\"כ ניצול (₪)", "סהכ ניצול (₪)", "סה\"כ ניצול"]),
    "utilization_pct": find_col(raw, ["% ניצול תקציב", "אחוז ניצול תקציב"]),
    "balance": find_col(raw, ["יתרה לניצול"]),
    "unreserved_balance": find_col(raw, ["יתרה לא משוריינת"]),
}

D = {
    "wbs": smart_find_col(det_raw, ["אלמנט WBS", "מספר WBS", "WBS"], ["wbs"]),
    "pi_name": smart_find_col(det_raw, ["שם חוקר ראשי", "חוקר ראשי"], ["חוקר"]),
    "protocol": smart_find_col(det_raw, ["מספר פרוטוקול", "סימון פרוטוקול"], ["פרוטוקול"]),
    "study_id": smart_find_col(det_raw, ["מספר הלסינקי", "study_id", "סוג תכנית-study_id", "סוג תכנית - study_id"], ["הלסינקי", "study_id", "סוג תכנית"]),
    "site": smart_find_col(det_raw, ["site", "SITE"], ["site"]),
    "budget_category": smart_find_col(det_raw, ["קטגוריית סעיף תקציבי", "סעיף תקציבי"], ["סעיף תקציבי", "קטגור"]),
    "commitment_group": smart_find_col(det_raw, ["קבוצת פריט התחייבות"], ["קבוצת פריט"]),
    "commitment_group_desc": smart_find_col(det_raw, ["תיאור קבוצת פריט התחייבות"], ["תיאור קבוצת"]),
    "description": smart_find_col(det_raw, ["תיאור"], ["תיאור"], ["קבוצת"]),
    "budget_total": smart_find_col(det_raw, ["סה\"כ תקציב מ", "סהכ תקציב מ", "סה\"כ תקציב", "סהכ תקציב", "תקציב", "תקציב מאושר", "סה\"כ תקציב מאושר", "סהכ תקציב מאושר"], ["תקציב"], ["יתרה", "ניצול", "אחוז", "%"]),
    "purchase_commitments": smart_find_col(det_raw, ["התחייבויות רכש", "התחייבות רכש", "התחייבויות", "התחייבות"], ["רכש", "התחייב"], ["יתרה", "ניצול", "אחוז", "%"]),
    "execution_total": smart_find_col(det_raw, ["סה\"כ ביצוע", "סהכ ביצוע", "ביצוע", "ביצוע בפועל", "סה\"כ ביצוע בפועל", "סהכ ביצוע בפועל"], ["ביצוע"], ["יתרה", "ניצול", "אחוז", "%"]),
    "balance": smart_find_col(det_raw, ["יתרה לניצול", "יתרה", "יתרת תקציב", "יתרה תקציבית"], ["יתרה"], ["אחוז", "%"]),
}

D = improve_payment_columns(det_raw, D)

# ============================================================
# CLEANING + CALCULATIONS
# ============================================================

numeric_cols = [
    C["expected_income"], C["actual_income"], C["total_expenses"],
    C["salary_expenses"], C["materials_expenses"], C["fixed_expenses"],
    C["travel_expenses"], C["internal_expenses"], C["expected_participants"],
    C["actual_participants"], C["unique_study"], C["unique_researcher"],
    C["budget"], C["overhead"], C["commitment"], C["execution"],
    C["utilization_total"], C["utilization_pct"], C["balance"], C["unreserved_balance"],
]

df = make_numeric(raw, numeric_cols)
details = make_numeric(det_raw, [D["budget_total"], D["purchase_commitments"], D["execution_total"], D["balance"]])

for dc in [C["approval_date"], C["start_date"], C["end_date"]]:
    if dc and dc in df.columns:
        df[dc] = pd.to_datetime(df[dc], errors="coerce", dayfirst=True)

if C["approval_year"] is None and C["approval_date"]:
    df["שנת אישור המחקר - מחושב"] = df[C["approval_date"]].dt.year
    C["approval_year"] = "שנת אישור המחקר - מחושב"

if C["approval_year"] and C["approval_year"] in df.columns:
    df[C["approval_year"]] = df[C["approval_year"]].astype(str).str.replace(".0", "", regex=False)

if C["utilization_pct"] and C["utilization_pct"] in df.columns:
    u = to_num(df[C["utilization_pct"]])
    df["% ניצול תקציב - מחושב"] = u * 100 if u.max() <= 1.5 and u.max() > 0 else u
elif C["budget"] and C["utilization_total"]:
    df["% ניצול תקציב - מחושב"] = np.where(to_num(df[C["budget"]]) > 0, to_num(df[C["utilization_total"]]) / to_num(df[C["budget"]]) * 100, 0)
else:
    df["% ניצול תקציב - מחושב"] = 0

df["סטטוס ניצול תקציב - מחושב"] = df["% ניצול תקציב - מחושב"].apply(budget_status)

if C["expected_participants"] and C["actual_participants"]:
    df["% גיוס משתתפים"] = np.where(to_num(df[C["expected_participants"]]) > 0, to_num(df[C["actual_participants"]]) / to_num(df[C["expected_participants"]]) * 100, 0)
else:
    df["% גיוס משתתפים"] = 0

df["סטטוס גיוס"] = df["% גיוס משתתפים"].apply(recruitment_status)

if C["end_date"] and C["end_date"] in df.columns:
    df["ימים לסיום"] = (df[C["end_date"]] - pd.Timestamp.today().normalize()).dt.days
else:
    df["ימים לסיום"] = np.nan

df["רמזור ניהולי"] = df.apply(
    lambda r: traffic_light(
        r["סטטוס ניצול תקציב - מחושב"],
        r[C["balance"]] if C["balance"] else None,
        r["ימים לסיום"],
        r["% גיוס משתתפים"],
    ),
    axis=1,
)

df["קבוצת מימון"] = df[C["funding_type"]].apply(funding_group) if C["funding_type"] else "לא סווג"
df = add_realization(df, C["expected_income"], C["actual_income"])

# ============================================================
# COLUMN LISTS
# ============================================================

study_cols = [
    C["study_id"], C["protocol"], C["pi"], C["department"], C["sponsor"],
    C["study_type"], C["funding_type"], "קבוצת מימון", C["approval_year"],
    C["expected_income"], C["actual_income"], "שיעור מימוש הכנסות",
    C["total_expenses"], C["expected_participants"], C["actual_participants"],
    "% גיוס משתתפים", "% ניצול תקציב - מחושב",
    "סטטוס ניצול תקציב - מחושב", "רמזור ניהולי",
]

budget_cols = [
    C["study_id"], C["protocol"], C["pi"], C["department"], C["sponsor"],
    C["funding_type"], "קבוצת מימון", C["wbs"], C["budget_name"],
    C["budget"], C["utilization_total"], "% ניצול תקציב - מחושב",
    C["balance"], C["unreserved_balance"], C["end_date"], "ימים לסיום",
    "סטטוס גיוס", "סטטוס ניצול תקציב - מחושב", "רמזור ניהולי",
]

researcher_cols = [
    C["study_id"], C["protocol"], C["sponsor"], C["funding_type"],
    "קבוצת מימון", C["wbs"], C["budget_name"], C["budget"],
    "% ניצול תקציב - מחושב", C["balance"],
    "סטטוס ניצול תקציב - מחושב", "רמזור ניהולי",
]

identity_cols = [
    C["study_id"], C["protocol"], C["pi"], C["department"], C["site"],
    C["sponsor"], C["study_type"], C["funding_type"], "קבוצת מימון",
    C["phase"], C["start_date"], C["end_date"], C["budget_name"],
    C["budget_owner"], C["wbs"], C["contract"], C["budget"], C["execution"],
    C["commitment"], C["utilization_total"], C["balance"], C["unreserved_balance"],
    "% ניצול תקציב - מחושב", C["expected_income"], C["actual_income"],
    "שיעור מימוש הכנסות", C["expected_participants"], C["actual_participants"],
    "% גיוס משתתפים", "סטטוס גיוס", "רמזור ניהולי",
]

payment_cols = [
    D["wbs"], D["study_id"], D["protocol"], D["pi_name"], D["site"],
    D["budget_category"], D["commitment_group"], D["commitment_group_desc"],
    D["description"], D["budget_total"], D["purchase_commitments"],
    D["execution_total"], D["balance"],
]

payment_cols_clean = clean_payment_columns(D)

money_cols = [
    C["expected_income"], C["actual_income"], C["total_expenses"], C["budget"],
    C["execution"], C["commitment"], C["utilization_total"], C["balance"],
    C["unreserved_balance"], D["budget_total"], D["purchase_commitments"],
    D["execution_total"], D["balance"],
]

pct_cols = ["% ניצול תקציב - מחושב", "% גיוס משתתפים", "שיעור מימוש הכנסות"]
num_cols2 = [C["expected_participants"], C["actual_participants"], "ימים לסיום"]
date_cols = [C["approval_date"], C["start_date"], C["end_date"]]

expense_map = {
    "שכר": C["salary_expenses"],
    "מתכלים": C["materials_expenses"],
    "קבוע": C["fixed_expenses"],
    "נסיעות": C["travel_expenses"],
    "העברות פנימיות": C["internal_expenses"],
}


def common_kpis(data, first_label="סה״כ מחקרים", first_val=None):
    exp = sum_col(data, C["expected_income"])
    act = sum_col(data, C["actual_income"])
    real = act / exp * 100 if exp > 0 else 0

    first_value = first_val if first_val is not None else study_count_by_year_text(data, C)

    kpis(
        [
            (first_label, first_value),
            ("צפי הכנסות", money(exp)),
            ("הכנסות בפועל", money(act)),
            ("מימוש הכנסות", pct(real)),
        ],
        columns_per_row=4,
    )


# ============================================================
# PAGES
# ============================================================

if page == "מנהלים":
    explain()
    common_kpis(df)
    render_insights("תובנות קצרות", insights(df, C))

    c1, c2 = st.columns(2)
    with c1:
        if C["approval_year"]:
            if C["unique_study"]:
                s = df.groupby(C["approval_year"], as_index=False)[C["unique_study"]].sum().rename(columns={C["approval_year"]: "שנה", C["unique_study"]: "מספר מחקרים"})
            else:
                s = df.groupby(C["approval_year"], as_index=False).size().rename(columns={C["approval_year"]: "שנה", "size": "מספר מחקרים"})
            chart_start(); bar(s, "שנה", "מספר מחקרים", "מגמת מחקרים לפי שנה", 360); chart_end()
    with c2:
        chart_start(); plot_realization_year(df, C["approval_year"], C["expected_income"], C["actual_income"]); chart_end()

    c3, c4 = st.columns(2)
    with c3:
        chart_start(); funding_chart(df, C["unique_study"]); chart_end()
    with c4:
        chart_start(); expense_chart(df, expense_map, "התפלגות הוצאות כללית"); chart_end()

    attention = df[df["רמזור ניהולי"].astype(str).str.contains("🔴|🟡", regex=True, na=False)]
    render_table(attention, "מחקרים לבדיקה תקציבית / גיוס", budget_cols, money_cols, pct_cols, num_cols2, date_cols)


elif page == "כלל בית החולים":
    explain()
    d = df.copy()

    with st.container(border=True):
        f1, f2, f3 = st.columns(3)
        with f1: d = filter_multi(d, "שנה", C["approval_year"], "h_y")
        with f2: d = filter_multi(d, "קבוצת מימון", "קבוצת מימון", "h_f")
        with f3: d = filter_multi(d, "סוג מחקר", C["study_type"], "h_t")

    common_kpis(d)
    render_insights("תובנות קצרות", insights(d, C))

    chart_start()
    studies_by_year_funding_bar(d, C, "סה״כ מחקרים לפי שנה וקבוצת מימון")
    chart_end()

    if C["approval_year"]:
        ycols = [x for x in [C["expected_income"], C["actual_income"], C["total_expenses"], C["overhead"]] if x]
        if ycols:
            ym = d.groupby(C["approval_year"], as_index=False)[ycols].sum().rename(columns={C["approval_year"]: "שנה"})
            chart_start(); grouped(ym, "שנה", ycols, "צפי הכנסות, הכנסות בפועל, הוצאות ותקורה לפי שנה"); chart_end()

    c3, c4 = st.columns(2)
    with c3:
        if C["pi"] and C["unique_study"]:
            s = d.groupby(C["pi"], as_index=False)[C["unique_study"]].sum().rename(columns={C["pi"]: "חוקר ראשי", C["unique_study"]: "מספר מחקרים"})
            chart_start(); top10(s, "חוקר ראשי", "מספר מחקרים", "Top 10 חוקרים לפי כמות מחקרים"); chart_end()
    with c4:
        if C["pi"] and C["expected_income"]:
            s = d.groupby(C["pi"], as_index=False)[C["expected_income"]].sum().rename(columns={C["pi"]: "חוקר ראשי", C["expected_income"]: "צפי הכנסות"})
            chart_start(); top10(s, "חוקר ראשי", "צפי הכנסות", "Top 10 חוקרים לפי צפי הכנסות"); chart_end()


elif page == "מחלקות":
    explain()
    d = df.copy()

    with st.container(border=True):
        f1, f2, f3 = st.columns(3)
        with f1: d, selected_department = filter_select(d, "מחלקה", C["department"], "d_sel")
        with f2: d = filter_multi(d, "שנה", C["approval_year"], "d_y")
        with f3: d = filter_multi(d, "קבוצת מימון", "קבוצת מימון", "d_f")

    common_kpis(d, "מחלקה", selected_department or "-")
    render_insights("תובנות קצרות", insights(d, C))

    c1, c2 = st.columns(2)
    with c1:
        chart_start(); studies_by_year_funding_bar(d, C, "מחקרים לפי שנה וקבוצת מימון במחלקה"); chart_end()
    with c2:
        chart_start(); expected_actual_by_year_chart(d, C, "הכנסות בפועל מול צפי הכנסות לפי שנה במחלקה"); chart_end()

    if C["approval_year"]:
        y = [x for x in [C["expected_income"], C["actual_income"], C["total_expenses"]] if x]
        if y:
            s = d.groupby(C["approval_year"], as_index=False)[y].sum().rename(columns={C["approval_year"]: "שנה"})
            chart_start(); grouped(s, "שנה", y, "הכנסות והוצאות לפי שנה במחלקה"); chart_end()

    render_table(d, "טבלת מחקרים במחלקה", study_cols, money_cols, pct_cols, num_cols2, date_cols)


elif page == "חוקרים":
    explain()
    d = df.copy()

    with st.container(border=True):
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            d = filter_multi(d, "מחלקה", C["department"], "p_dept")
        with f2:
            d, selected_pi = filter_select(d, "חוקר ראשי", C["pi"], "p_sel")
        with f3:
            d = filter_multi(d, "שנה", C["approval_year"], "p_y")
        with f4:
            d = filter_multi(d, "קבוצת מימון", "קבוצת מימון", "p_f")

    common_kpis(d, "חוקר", selected_pi or "-")
    render_insights("תובנות קצרות", insights(d, C))

    c1, c2 = st.columns(2)
    with c1:
        chart_start(); studies_by_year_funding_bar(d, C, "מחקרים לפי שנה וקבוצת מימון לחוקר"); chart_end()
    with c2:
        chart_start(); expense_stacked_by_year_chart(d, C, expense_map, "התפלגות הוצאות לחוקר לפי שנה וסוג הוצאה"); chart_end()

    if C["study_id"] and not d.empty:
        opts = ["כל המחקרים"] + sorted(d[C["study_id"]].dropna().apply(clean_key).unique().tolist())
        chosen = st.selectbox("בחירת מחקר להצגת התפלגות הוצאות ממוקדת", opts, key="exp_study")
        if chosen != "כל המחקרים":
            selected_study_df = d[d[C["study_id"]].apply(clean_key) == chosen]
            chart_start(); expense_chart(selected_study_df, expense_map, f"התפלגות הוצאות למחקר {chosen}"); chart_end()

    if C["approval_year"]:
        y = [x for x in [C["expected_income"], C["actual_income"], C["total_expenses"]] if x]
        if y:
            s = d.groupby(C["approval_year"], as_index=False)[y].sum().rename(columns={C["approval_year"]: "שנה"})
            chart_start(); grouped(s, "שנה", y, "הכנסות מול הוצאות לפי שנה לחוקר"); chart_end()

    render_table(d, "טבלת מחקרים לחוקר", study_cols, money_cols, pct_cols, num_cols2, date_cols)


elif page == "יזמים":
    d = df.copy()

    with st.container(border=True):
        f1, f2 = st.columns(2)
        with f1: d = filter_multi(d, "יזם", C["sponsor"], "s_s")
        with f2: d = filter_multi(d, "שנה", C["approval_year"], "s_y")

    if C["sponsor"]:
        if C["unique_study"]:
            s = d.groupby(C["sponsor"], as_index=False)[C["unique_study"]].sum().rename(columns={C["sponsor"]: "יזם", C["unique_study"]: "מספר מחקרים סה״כ"})
        elif C["study_id"]:
            temp = d[[C["sponsor"], C["study_id"]]].copy()
            temp["__id__"] = temp[C["study_id"]].apply(clean_key)
            temp = temp[temp["__id__"] != ""]
            s = temp.groupby(C["sponsor"], as_index=False)["__id__"].nunique().rename(columns={C["sponsor"]: "יזם", "__id__": "מספר מחקרים סה״כ"})
        else:
            s = d.groupby(C["sponsor"], as_index=False).size().rename(columns={C["sponsor"]: "יזם", "size": "מספר מחקרים סה״כ"})

        if C["approval_year"]:
            if C["unique_study"]:
                ytbl = d.pivot_table(index=C["sponsor"], columns=C["approval_year"], values=C["unique_study"], aggfunc="sum", fill_value=0)
            elif C["study_id"]:
                temp = d[[C["sponsor"], C["approval_year"], C["study_id"]]].copy()
                temp["__id__"] = temp[C["study_id"]].apply(clean_key)
                temp = temp[temp["__id__"] != ""]
                ytbl = temp.pivot_table(index=C["sponsor"], columns=C["approval_year"], values="__id__", aggfunc=pd.Series.nunique, fill_value=0)
            else:
                ytbl = d.pivot_table(index=C["sponsor"], columns=C["approval_year"], aggfunc="size", fill_value=0)
            ytbl.columns = [f"מספר מחקרים {safe_display(c)}" for c in ytbl.columns]
            ytbl = ytbl.reset_index().rename(columns={C["sponsor"]: "יזם"})
            s = s.merge(ytbl, on="יזם", how="left")

        for col, name in [(C["expected_income"], "צפי הכנסות"), (C["actual_income"], "הכנסות בפועל"), (C["total_expenses"], "סך הוצאות")]:
            if col:
                temp = d.groupby(C["sponsor"], as_index=False)[col].sum().rename(columns={C["sponsor"]: "יזם", col: name})
                s = s.merge(temp, on="יזם", how="left")

        s = s.sort_values("מספר מחקרים סה״כ", ascending=False)
        real = s["הכנסות בפועל"].sum() / s["צפי הכנסות"].sum() * 100 if "הכנסות בפועל" in s.columns and "צפי הכנסות" in s.columns and s["צפי הכנסות"].sum() > 0 else 0

        kpis([
            ("מספר יזמים", number(s["יזם"].nunique())),
            ("סה״כ מחקרים", number(s["מספר מחקרים סה״כ"].sum())),
            ("צפי הכנסות", money(s.get("צפי הכנסות", pd.Series([0])).sum())),
            ("מימוש הכנסות", pct(real)),
        ])

        c1, c2 = st.columns(2)
        with c1:
            chart_start(); top10(s, "יזם", "מספר מחקרים סה״כ", "Top 10 יזמים לפי כמות מחקרים"); chart_end()
        with c2:
            if "צפי הכנסות" in s.columns:
                chart_start(); top10(s, "יזם", "צפי הכנסות", "Top 10 יזמים לפי צפי הכנסות"); chart_end()

        year_count_cols = [c for c in s.columns if str(c).startswith("מספר מחקרים ")]
        render_table(
            s,
            "טבלת סיכום יזמים",
            money_cols=["צפי הכנסות", "הכנסות בפועל", "סך הוצאות"],
            num_cols=["מספר מחקרים סה״כ"] + year_count_cols,
        )


elif page == "סטטוס תקציב וגיוס":
    explain()
    d = df.copy()

    with st.container(border=True):
        f1, f2, f3 = st.columns(3)
        with f1: d = filter_multi(d, "שנה", C["approval_year"], "t_y")
        with f2: d = filter_multi(d, "מחלקה", C["department"], "t_d")
        with f3: d = filter_multi(d, "חוקר ראשי", C["pi"], "t_p")

        f4, f5, f6 = st.columns(3)
        with f4: d = filter_multi(d, "קבוצת מימון", "קבוצת מימון", "t_f")
        with f5: d = filter_multi(d, "סטטוס ניצול", "סטטוס ניצול תקציב - מחושב", "t_u")
        with f6: d = filter_multi(d, "סטטוס גיוס", "סטטוס גיוס", "t_r")

    over = d[d["סטטוס ניצול תקציב - מחושב"] == "חריגה"]
    high = d[d["סטטוס ניצול תקציב - מחושב"] == "קרוב לניצול מלא"]
    low = d[d["סטטוס ניצול תקציב - מחושב"] == "ניצול נמוך"]
    lowrec = d[d["סטטוס גיוס"].isin(["אין גיוס", "גיוס נמוך"])]
    soon = d[(d["ימים לסיום"] >= 0) & (d["ימים לסיום"] <= 60)]

    kpis([
        ("חריגה תקציבית", number(len(over))),
        ("קרוב לניצול מלא", number(len(high))),
        ("ניצול נמוך", number(len(low))),
        ("גיוס נמוך / אין גיוס", number(len(lowrec))),
    ], columns_per_row=4)

    c1, c2 = st.columns(2)
    with c1:
        s = d.groupby("סטטוס ניצול תקציב - מחושב", as_index=False).size().rename(columns={"size": "מספר מחקרים"})
        chart_start(); donut(s, "סטטוס ניצול תקציב - מחושב", "מספר מחקרים", "התפלגות סטטוס ניצול תקציבי"); chart_end()
    with c2:
        s = d.groupby("סטטוס גיוס", as_index=False).size().rename(columns={"size": "מספר מחקרים"})
        chart_start(); donut(s, "סטטוס גיוס", "מספר מחקרים", "התפלגות סטטוס גיוס"); chart_end()

    choice = st.radio(
        "יש לבחור סוג בדיקה להצגה",
        ["חריגה תקציבית", "קרוב לניצול מלא", "ניצול נמוך", "גיוס נמוך", "סיום קרוב", "כל הסטטוסים"],
        horizontal=True,
    )

    if choice == "חריגה תקציבית": table, title = over, "מחקרים בחריגה תקציבית"
    elif choice == "קרוב לניצול מלא": table, title = high, "מחקרים קרובים לניצול מלא"
    elif choice == "ניצול נמוך": table, title = low, "מחקרים בניצול נמוך"
    elif choice == "גיוס נמוך": table, title = lowrec, "מחקרים עם גיוס נמוך / ללא גיוס"
    elif choice == "סיום קרוב": table, title = soon, "מחקרים שמסתיימים תוך 60 יום"
    else: table, title = d, "טבלת סטטוס תקציב וגיוס"

    render_table(table, title, budget_cols, money_cols, pct_cols, num_cols2, date_cols)


elif page == "דוח חוקר":
    explain()
    d = df.copy()

    with st.container(border=True):
        f1, f2, f3, f4 = st.columns(4)
        with f1: d = filter_multi(d, "מחלקה", C["department"], "r_dept")
        with f2: d, selected_researcher = filter_select(d, "בחירת חוקר", C["pi"], "r_sel")
        with f3: d = filter_multi(d, "שנה", C["approval_year"], "r_y")
        with f4: d = filter_multi(d, "קבוצת מימון", "קבוצת מימון", "r_f")

    if d.empty:
        st.info("לא נמצאו מחקרים להצגה.")
        st.stop()

    exp = sum_col(d, C["expected_income"])
    act = sum_col(d, C["actual_income"])

    kpis([
        ("חוקר", selected_researcher or "-"),
        ("מספר מחקרים", number(count_studies(d, C["unique_study"], C["study_id"]))),
        ("תקציב כולל", money(sum_col(d, C["budget"]))),
        ("מימוש הכנסות", pct(act / exp * 100 if exp > 0 else 0)),
    ], columns_per_row=4)

    render_table(d, "רשימת מחקרים לחוקר", researcher_cols, money_cols, pct_cols, num_cols2, date_cols, 280)

    st.markdown("### בחירת מחקר לפתיחת תעודת זהות")

    if C["study_id"] and C["study_id"] in d.columns:
        study_options_df = d.copy()
        study_options_df["__study_key__"] = study_options_df[C["study_id"]].apply(clean_key)
        if C["protocol"] and C["protocol"] in study_options_df.columns:
            study_options_df["__display__"] = study_options_df["__study_key__"] + " | " + study_options_df[C["protocol"]].astype(str).fillna("")
        else:
            study_options_df["__display__"] = study_options_df["__study_key__"]
        study_options_df = study_options_df.drop_duplicates("__study_key__")
        study_options = study_options_df["__display__"].dropna().tolist()
        selected_display = st.selectbox("יש לבחור מחקר ספציפי", study_options, key="researcher_specific_study")
        selected_study_key = selected_display.split(" | ")[0].strip()
        one = d[d[C["study_id"]].apply(clean_key) == selected_study_key]
    else:
        st.warning("לא נמצאה עמודת מספר הלסינקי ולכן לא ניתן לפתוח תעודת זהות למחקר.")
        one = pd.DataFrame()
        selected_study_key = ""

    if not one.empty:
        r = one.iloc[0]
        st.markdown("### תעודת זהות למחקר")

        cards = [
            ("מספר הלסינקי", r.get(C["study_id"], "")),
            ("מספר פרוטוקול", r.get(C["protocol"], "") if C["protocol"] else ""),
            ("חוקר ראשי", r.get(C["pi"], "") if C["pi"] else ""),
            ("מחלקה", r.get(C["department"], "") if C["department"] else ""),
            ("יזם", r.get(C["sponsor"], "") if C["sponsor"] else ""),
            ("קבוצת מימון", r.get("קבוצת מימון", "")),
            ("WBS", r.get(C["wbs"], "") if C["wbs"] else ""),
            ("שם תקציב", r.get(C["budget_name"], "") if C["budget_name"] else ""),
            ("תקציב", money(r.get(C["budget"], 0)) if C["budget"] else "0 ₪"),
            ("סה״כ ניצול", money(r.get(C["utilization_total"], 0)) if C["utilization_total"] else "0 ₪"),
            ("יתרה", money(r.get(C["balance"], 0)) if C["balance"] else "0 ₪"),
            ("מימוש הכנסות", pct(r.get("שיעור מימוש הכנסות", 0))),
            ("רמזור", r.get("רמזור ניהולי", "")),
        ]
        render_identity_cards(cards)

        pay = payment_for(details, one, C, D, selected_researcher)

        c1, c2 = st.columns(2)
        with c1:
            chart_start(); budget_exec_chart(pay, D); chart_end()
        with c2:
            chart_start(); expense_chart(one, expense_map, f"התפלגות הוצאות למחקר {selected_study_key}"); chart_end()

        render_table(one, "פרטים מלאים למחקר שנבחר", identity_cols, money_cols, pct_cols, num_cols2, date_cols, 330)

        if pay is not None and not pay.empty:
            pay_display = ensure_payment_display_columns(pay, one, C, D)
            render_table(pay_display, "פירוט הוצאות והכנסות מתוך גיליון הפירוט", payment_cols_clean, money_cols, pct_cols, num_cols2, date_cols, 330)


elif page == "מעקב הוצאות והכנסות":
    source = df.copy()

    with st.container(border=True):
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            source = filter_multi(source, "מחלקה", C["department"], "pay_dept")
        with f2:
            source, selected_researcher = filter_select(source, "חוקר", C["pi"], "pay_sel")
        with f3:
            source = filter_multi(source, "שנה", C["approval_year"], "pay_year")
        with f4:
            source = filter_multi(source, "קבוצת מימון", "קבוצת מימון", "pay_funding")

    pay = payment_for(details, source, C, D, selected_researcher)

    if pay.empty and not details.empty:
        st.warning(
            f"לא נמצאה התאמה מדויקת לגיליון הפירוט לפי חוקר/מחקר. "
            f"נמצאו {len(details):,} שורות בגיליון הפירוט, אך 0 שורות לאחר הסינון. "
            f"בדקי שהעמודות מספר הלסינקי/פרוטוקול/WBS/חוקר זהות בין הגיליונות."
        )
        pay = get_department_from_source(details, source, C, D)

    if D["study_id"] and D["study_id"] in pay.columns and not pay.empty:
        pay = filter_multi(pay, "מחקר", D["study_id"], "pay_study")

    with st.expander("בדיקת זיהוי עמודות בגיליון פירוט הוצאות והכנסות", expanded=False):
        st.write("גיליון פירוט שזוהה:", details_sheet)
        st.write({
            "WBS": D.get("wbs"),
            "חוקר": D.get("pi_name"),
            "מספר הלסינקי/study_id": D.get("study_id"),
            "מספר פרוטוקול": D.get("protocol"),
            "סה״כ תקציב": D.get("budget_total"),
            "התחייבויות רכש": D.get("purchase_commitments"),
            "סה״כ ביצוע": D.get("execution_total"),
            "יתרה לניצול": D.get("balance"),
            "שורות לאחר סינון": len(pay),
            "שורות בגיליון הפירוט": len(details),
        })

    kpis([
        ("חוקר", selected_researcher or "-"),
        ("סה״כ תקציב", money(sum_col(pay, D["budget_total"]))),
        ("התחייבויות רכש", money(sum_col(pay, D["purchase_commitments"]))),
        ("סה״כ ביצוע", money(sum_col(pay, D["execution_total"]))),
    ], columns_per_row=4)

    chart_start()
    budget_exec_chart(pay, D)
    chart_end()

    if D["budget_category"] and D["budget_category"] in pay.columns:
        y = [D["budget_total"], D["purchase_commitments"], D["execution_total"], D["balance"]]
        y = [x for x in y if x and x in pay.columns]

        if y:
            cat = (
                pay.groupby(D["budget_category"], as_index=False)[y]
                .sum()
                .rename(columns={D["budget_category"]: "קטגוריית סעיף תקציבי"})
            )

            c1, c2 = st.columns(2)

            with c1:
                render_table(cat, "סיכום לפי קטגוריית סעיף תקציבי", money_cols=y, height=310)

            with c2:
                chart_start()
                grouped(cat, "קטגוריית סעיף תקציבי", y, "תקציב, התחייבויות, ביצוע ויתרה לפי קטגוריה", 360)
                chart_end()

    if D["wbs"] and D["wbs"] in pay.columns:
        y = [D["budget_total"], D["purchase_commitments"], D["execution_total"], D["balance"]]
        y = [x for x in y if x and x in pay.columns]

        if y:
            wbs_summary = (
                pay.groupby(D["wbs"], as_index=False)[y]
                .sum()
                .rename(columns={D["wbs"]: "אלמנט WBS"})
            )

            render_table(wbs_summary, "סיכום לפי WBS", money_cols=y, height=300)

    pay_display = ensure_payment_display_columns(pay, source, C, D)
    render_table(pay_display, "טבלת פירוט הוצאות והכנסות פר מחקר", payment_cols_clean, money_cols, pct_cols, num_cols2, date_cols)
