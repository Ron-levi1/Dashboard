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
    initial_sidebar_state="expanded",
)

APP_VERSION = "v8-polished-financial-dashboard-2026-06-09"


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>
html, body, [class*="css"] {
    direction: rtl;
    text-align: right;
    font-family: Arial, sans-serif;
    background: #f3f6fb;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1620px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0f172a,#1e293b);
}

section[data-testid="stSidebar"] * {
    color: white;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
    background: rgba(255,255,255,.07);
    border-radius: 12px;
    padding: 8px 10px;
    margin-bottom: 6px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,.14);
}

.hero {
    background: linear-gradient(135deg,#0f172a,#1e3a8a 48%,#0f766e);
    color: white;
    padding: 30px 36px;
    border-radius: 28px;
    margin-bottom: 22px;
    box-shadow: 0 18px 42px rgba(15,23,42,.22);
}

.hero h1 {
    color: white;
    font-size: 2.15rem;
    margin: 0 0 8px 0;
    font-weight: 900;
}

.hero p {
    color: #dbeafe;
    margin: 0;
}

.page-header {
    background: #fff;
    border: 1px solid #dbe3ef;
    border-right: 7px solid #2563eb;
    border-radius: 24px;
    padding: 20px 24px;
    margin-bottom: 18px;
    box-shadow: 0 10px 26px rgba(15,23,42,.055);
}

.page-header h2 {
    color: #0f172a;
    font-size: 1.55rem;
    font-weight: 950;
    margin: 0 0 6px 0;
}

.page-header p {
    color: #64748b;
    margin: 0;
}

div[data-testid="stMetric"] {
    background: linear-gradient(135deg,#fff,#f8fafc);
    border: 1px solid #dbe3ef;
    padding: 16px;
    border-radius: 20px;
    box-shadow: 0 8px 24px rgba(15,23,42,.055);
    min-height: 104px;
}

div[data-testid="stMetricLabel"] {
    color: #64748b;
    font-weight: 800;
}

div[data-testid="stMetricValue"] {
    color: #0f172a;
    font-size: 1.28rem;
    font-weight: 950;
}

.insight-box {
    background: #fff;
    border: 1px solid #dbe3ef;
    border-radius: 22px;
    padding: 18px 20px;
    margin-bottom: 18px;
    box-shadow: 0 8px 24px rgba(15,23,42,.05);
    direction: rtl;
    text-align: right;
}

.insight-title {
    color: #0f172a;
    font-size: 1.12rem;
    font-weight: 950;
    margin-bottom: 10px;
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

.chart-card,
div[data-testid="stFileUploader"],
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #fff !important;
    border: 1px solid #dbe3ef !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 20px rgba(15,23,42,.04);
}

.chart-card {
    padding: 16px 18px 8px 18px;
    margin-bottom: 18px;
}

div[data-testid="stFileUploader"] {
    padding: 18px !important;
    margin-bottom: 22px !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    margin-bottom: 18px !important;
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

.table-title {
    color: #0f172a;
    font-size: 1.18rem;
    font-weight: 950;
    margin: 18px 0 10px 0;
}

.identity-grid {
    display: grid;
    grid-template-columns: repeat(4,minmax(190px,1fr));
    gap: 14px;
    margin: 10px 0 20px;
}

.identity-card {
    background: #fff;
    border: 1px solid #dbe3ef;
    border-radius: 18px;
    padding: 14px 16px;
    box-shadow: 0 8px 22px rgba(15,23,42,.045);
    min-height: 88px;
}

.identity-label {
    color: #64748b;
    font-size: .82rem;
    font-weight: 800;
    margin-bottom: 8px;
}

.identity-value {
    color: #0f172a;
    font-size: 1.02rem;
    font-weight: 900;
    word-break: break-word;
}

.small-note {
    color: #64748b;
    font-size: 0.88rem;
    margin-top: -4px;
    margin-bottom: 10px;
}

@media(max-width:1000px) {
    .identity-grid {
        grid-template-columns: repeat(2,1fr);
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# BASIC HELPERS
# ============================================================


def norm(v):
    if pd.isna(v):
        return ""
    v = str(v)
    v = v.replace("\u200f", "").replace("\u200e", "")
    v = v.replace("–", "-").replace("—", "-").replace("−", "-")
    return " ".join(v.split()).strip()


def normalize_columns(df):
    df = df.copy()
    df.columns = [norm(c) for c in df.columns]
    return df


def find_col(df, names):
    normalized = {norm(c): c for c in df.columns}
    for n in names:
        n = norm(n)
        if n in normalized:
            return normalized[n]
    return None


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
    return s


def to_num(s):
    return (
        s.astype(str)
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
    if col and col in df.columns:
        return to_num(df[col]).sum()
    return 0


def count_studies(df, uniq=None, study_id=None):
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


# ============================================================
# DISPLAY HELPERS
# ============================================================


def format_df(data, money_cols=None, pct_cols=None, num_cols=None, date_cols=None):
    money_cols = money_cols or []
    pct_cols = pct_cols or []
    num_cols = num_cols or []
    date_cols = date_cols or []

    out = data.copy()

    for c in out.columns:
        if c in money_cols:
            out[c] = out[c].apply(money)
        elif c in pct_cols:
            out[c] = out[c].apply(pct)
        elif c in num_cols:
            out[c] = out[c].apply(number)
        elif c in date_cols:
            out[c] = pd.to_datetime(out[c], errors="coerce").dt.strftime("%d/%m/%Y").fillna("")
        else:
            out[c] = out[c].apply(clean_key)

    return out


def render_table(df, title, cols=None, money_cols=None, pct_cols=None, num_cols=None, date_cols=None, height=430):
    st.markdown(f'<div class="table-title">{title}</div>', unsafe_allow_html=True)

    if df is None or df.empty:
        st.info("אין נתונים להצגה בהתאם לבחירה הנוכחית.")
        return

    data = df.copy()

    if cols:
        cols = [c for c in cols if c and c in data.columns]
        if cols:
            data = data[cols]

    data = format_df(data, money_cols, pct_cols, num_cols, date_cols)
    st.dataframe(data, use_container_width=True, height=height, hide_index=True)


def kpis(items, columns_per_row=4):
    if not items:
        return

    for start in range(0, len(items), columns_per_row):
        chunk = items[start:start + columns_per_row]
        cols = st.columns(len(chunk))

        for c, (label, value) in zip(cols, chunk):
            with c:
                with st.container(border=True):
                    st.metric(label, value)


def page_header(title, subtitle):
    st.markdown(
        f"""
        <div class="page-header">
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_start():
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)


def chart_end():
    st.markdown("</div>", unsafe_allow_html=True)


def base(fig, h=400):
    fig.update_layout(
        height=h,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(size=13, color="#334155"),
        title=dict(x=0.5, font=dict(size=18, color="#0f172a")),
        margin=dict(l=40, r=40, t=80, b=60),
        legend=dict(title=""),
    )
    return fig


def bar(df, x, y, title, h=390, color="#2563eb"):
    if df is None or df.empty or x not in df.columns or y not in df.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    d = df.copy()
    d[x] = d[x].astype(str)
    d["תווית"] = d[y].apply(compact)

    fig = px.bar(d, x=x, y=y, text="תווית", title=title)
    fig.update_traces(textposition="outside", cliponaxis=False, marker_color=color)
    fig.update_layout(xaxis=dict(type="category"), yaxis=dict(gridcolor="#e2e8f0"), bargap=0.38)
    st.plotly_chart(base(fig, h), use_container_width=True)


def grouped(df, x, ycols, title, h=430):
    ycols = [c for c in ycols if c and c in df.columns]

    if df is None or df.empty or not ycols:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    m = df.melt(id_vars=[x], value_vars=ycols, var_name="מדד", value_name="ערך")
    m["תווית"] = m["ערך"].apply(compact)

    fig = px.bar(
        m,
        x=x,
        y="ערך",
        color="מדד",
        barmode="group",
        text="תווית",
        title=title,
        color_discrete_sequence=["#1d4ed8", "#38bdf8", "#ef4444", "#a78bfa", "#10b981"],
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(xaxis=dict(type="category"), yaxis=dict(gridcolor="#e2e8f0"), bargap=0.34)
    st.plotly_chart(base(fig, h), use_container_width=True)


def donut(df, names, values, title, h=380):
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
    st.plotly_chart(base(fig, h), use_container_width=True)


def top10(df, label, value, title):
    if df is None or df.empty or label not in df.columns or value not in df.columns:
        st.info("אין מספיק נתונים להצגת הגרף.")
        return

    d = df.sort_values(value).tail(10).copy()
    d["שם מקוצר"] = d[label].astype(str).apply(lambda s: s[:25] + "..." if len(s) > 28 else s)
    d["תווית"] = d[value].apply(compact)

    fig = px.bar(d, x=value, y="שם מקוצר", orientation="h", text="תווית", title=title, hover_data={label: True})
    fig.update_traces(textposition="outside", cliponaxis=False, marker_color="#2563eb")
    fig.update_layout(yaxis=dict(title=""), xaxis=dict(gridcolor="#e2e8f0"), showlegend=False)
    st.plotly_chart(base(fig, max(420, len(d) * 48 + 140)), use_container_width=True)


def explain():
    with st.expander("ℹ️ הסבר על המדדים בדשבורד", expanded=False):
        st.markdown(
            """
            <div style="direction:rtl;text-align:right;line-height:1.8">
            <b>שיעור מימוש הכנסות</b> = הכנסות בפועל / צפי הכנסות × 100.<br>
            <b>סטטוס ניצול תקציב</b> = סה״כ ניצול / תקציב × 100.
            עד 20% ניצול נמוך, 20%–80% תקין, 80%–100% קרוב לניצול מלא, מעל 100% חריגה.<br>
            <b>סטטוס גיוס משתתפים</b> = משתתפים בפועל / צפי משתתפים × 100.<br>
            <b>מחקרי יזם / גרנט</b> מסווגים לפי עמודת סוג המימון.
            </div>
            """,
            unsafe_allow_html=True,
        )


def insights(df, C):
    out = []
    total = count_studies(df, C.get("unique_study"), C.get("study_id"))
    exp = sum_col(df, C.get("expected_income"))
    act = sum_col(df, C.get("actual_income"))
    exps = sum_col(df, C.get("total_expenses"))

    out.append((f"סה״כ מוצגים {number(total)} מחקרים בהתאם לסינון הנוכחי.", "success"))

    if exp > 0:
        r = act / exp * 100
        kind = "success" if r >= 80 else "warning" if r >= 50 else "danger"
        out.append((f"שיעור מימוש ההכנסות בפועל מתוך צפי ההכנסות הוא {pct(r)}.", kind))

    if act > 0:
        er = exps / act * 100
        kind = "danger" if er > 90 else "warning" if er > 70 else "success"
        out.append((f"שיעור ההוצאות מתוך ההכנסות בפועל הוא {pct(er)}.", kind))

    if "קבוצת מימון" in df.columns:
        s = df.groupby("קבוצת מימון").size().sort_values(ascending=False)
        if not s.empty:
            out.append((f"קבוצת המימון הדומיננטית היא {s.index[0]}, עם {number(s.iloc[0])} רשומות.", "success"))

    if "סטטוס ניצול תקציב - מחושב" in df.columns:
        n = len(df[df["סטטוס ניצול תקציב - מחושב"] == "חריגה"])
        if n:
            out.append((f"{number(n)} מחקרים נמצאים בחריגה תקציבית ודורשים בדיקה.", "danger"))

    if "סטטוס גיוס" in df.columns:
        n = len(df[df["סטטוס גיוס"].isin(["אין גיוס", "גיוס נמוך"])])
        if n:
            out.append((f"{number(n)} מחקרים עם גיוס נמוך או ללא גיוס.", "warning"))

    return out


def render_insights(title, items):
    html = f'<div class="insight-box"><div class="insight-title">{title}</div>'
    for txt, kind in items:
        html += f'<div class="insight-item insight-{kind}">{txt}</div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def download_excel(sheets):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for name, data in sheets.items():
            if data is None:
                data = pd.DataFrame()
            data.to_excel(writer, index=False, sheet_name=str(name)[:31])
    return output.getvalue()


def filter_select(df, label, col, key):
    if not col or col not in df.columns:
        return df, None

    vals = sorted(df[col].dropna().astype(str).unique())
    if not vals:
        return df.iloc[0:0], None

    sel = st.selectbox(label, vals, key=key)
    return df[df[col].astype(str) == sel], sel


def filter_multi(df, label, col, key, default_all=False):
    if not col or col not in df.columns:
        return df

    vals = sorted(df[col].dropna().astype(str).unique())
    if not vals:
        return df.iloc[0:0]

    selected = st.multiselect(label, vals, default=vals if default_all else [], key=key, placeholder="בחרי ערכים לסינון")

    if selected:
        return df[df[col].astype(str).isin(selected)]

    return df


def payment_for(details, source, C, D, researcher=None):
    d = details.copy()
    masks = []

    if C.get("study_id") and D.get("study_id") and C["study_id"] in source.columns and D["study_id"] in d.columns:
        ids = set(source[C["study_id"]].dropna().apply(clean_key))
        masks.append(d[D["study_id"]].apply(clean_key).isin(ids))

    if C.get("protocol") and D.get("protocol") and C["protocol"] in source.columns and D["protocol"] in d.columns:
        ps = set(source[C["protocol"]].dropna().apply(clean_key))
        masks.append(d[D["protocol"]].apply(clean_key).isin(ps))

    if researcher and D.get("pi_name") and D["pi_name"] in d.columns:
        masks.append(d[D["pi_name"]].astype(str) == str(researcher))

    if masks:
        m = masks[0]
        for x in masks[1:]:
            m = m | x
        d = d[m]

    return d


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
    fig.update_traces(textposition="outside", cliponaxis=False, marker_color="#0f766e")
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
    for name, key in [("תקציב", "budget_total"), ("התחייבויות רכש", "purchase_commitments"), ("ביצוע", "execution_total"), ("יתרה לניצול", "balance")]:
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
        s,
        x="מדד",
        y="סכום",
        text="תווית",
        title="תקציב מול התחייבויות רכש, ביצוע ויתרה",
        color="מדד",
        color_discrete_sequence=["#1d4ed8", "#f59e0b", "#ef4444", "#10b981"],
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(showlegend=False, yaxis=dict(gridcolor="#e2e8f0"))
    st.plotly_chart(base(fig, 390), use_container_width=True)


# ============================================================
# NAVIGATION
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
            "🚦 בקרת תקציב וגיוס",
            "🧾 דוח חוקר",
            "💳 מעקב דרישות תשלום",
        ],
        label_visibility="collapsed",
    )

st.markdown(
    f"""
    <div class="hero">
        <h1>📊 דשבורד ניהולי למחקרים קליניים</h1>
        <p>תצוגת הנהלה למחקרים, תקציבים, הכנסות, הוצאות, חוקרים, מחלקות ויזמים | {APP_VERSION}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader("העלי קובץ Excel", type=["xlsx"])
if uploaded_file is None:
    st.info("יש להעלות קובץ Excel כדי להתחיל.")
    st.stop()


# ============================================================
# READ EXCEL
# ============================================================

try:
    xls = pd.ExcelFile(uploaded_file)
    studies_sheet = next((s for s in xls.sheet_names if norm(s).lower() == "studies_data"), xls.sheet_names[0])
    detail_candidates = [s for s in xls.sheet_names if s != studies_sheet]
    details_sheet = detail_candidates[0] if detail_candidates else studies_sheet

    for s in detail_candidates:
        sample = normalize_columns(pd.read_excel(xls, sheet_name=s, nrows=10))
        if find_col(sample, ["קטגוריית סעיף תקציבי"]) or find_col(sample, ["מספר הלסינקי"]):
            details_sheet = s
            break

    raw = normalize_columns(pd.read_excel(xls, sheet_name=studies_sheet))
    det_raw = normalize_columns(pd.read_excel(xls, sheet_name=details_sheet))

except Exception as e:
    st.error("לא הצלחתי לקרוא את קובץ האקסל.")
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
    "study_id": find_col(raw, ["סוג תכנית-study_id", "סוג תכנית – study_id", "סוג תכנית - study_id", "מספר הלסינקי"]),
    "pi": find_col(raw, ["חוקר ראשי", "שם חוקר ראשי"]),
    "site": find_col(raw, ["site", "SITE"]),
    "department": find_col(raw, ["מחלקה"]),
    "study_type": find_col(raw, ["סוג המחקר"]),
    "phase": find_col(raw, ["פאזת המחקר", "פאזה"]),
    "sponsor": find_col(raw, ["יזם", "גורם מממן"]),
    "funding_type": find_col(raw, ["סוג מימון"]),
    "expected_income": find_col(raw, ["צפי הכנסות (₪)", "צפי הכנסות ₪", "צפי הכנסות"]),
    "actual_income": find_col(raw, ["הכנסות בפועל"]),
    "total_expenses": find_col(raw, ["סך ההוצאות"]),
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
    "wbs": find_col(det_raw, ["אלמנט WBS", "מספר WBS"]),
    "pi_name": find_col(det_raw, ["שם חוקר ראשי", "חוקר ראשי"]),
    "protocol": find_col(det_raw, ["מספר פרוטוקול"]),
    "study_id": find_col(det_raw, ["מספר הלסינקי"]),
    "site": find_col(det_raw, ["site", "SITE"]),
    "budget_category": find_col(det_raw, ["קטגוריית סעיף תקציבי"]),
    "commitment_group": find_col(det_raw, ["קבוצת פריט התחייבות"]),
    "commitment_group_desc": find_col(det_raw, ["תיאור קבוצת פריט התחייבות"]),
    "description": find_col(det_raw, ["תיאור"]),
    "budget_total": find_col(det_raw, ["סה\"כ תקציב מ", "סהכ תקציב מ"]),
    "purchase_commitments": find_col(det_raw, ["התחייבויות רכש"]),
    "execution_total": find_col(det_raw, ["סה\"כ ביצוע", "סהכ ביצוע"]),
    "balance": find_col(det_raw, ["יתרה לניצול"]),
}


# ============================================================
# CLEANING + CALCULATIONS
# ============================================================

num_cols = [
    C["expected_income"], C["actual_income"], C["total_expenses"],
    C["salary_expenses"], C["materials_expenses"], C["fixed_expenses"],
    C["travel_expenses"], C["internal_expenses"], C["expected_participants"],
    C["actual_participants"], C["unique_study"], C["unique_researcher"],
    C["budget"], C["overhead"], C["commitment"], C["execution"],
    C["utilization_total"], C["utilization_pct"], C["balance"], C["unreserved_balance"],
]

df = make_numeric(raw, num_cols)
details = make_numeric(det_raw, [D["budget_total"], D["purchase_commitments"], D["execution_total"], D["balance"]])

for dc in [C["approval_date"], C["start_date"], C["end_date"]]:
    if dc and dc in df.columns:
        df[dc] = pd.to_datetime(df[dc], errors="coerce", dayfirst=True)

if C["approval_year"] is None and C["approval_date"]:
    df["שנת אישור המחקר - מחושב"] = df[C["approval_date"]].dt.year
    C["approval_year"] = "שנת אישור המחקר - מחושב"

if C["approval_year"]:
    df[C["approval_year"]] = df[C["approval_year"]].astype(str).str.replace(".0", "", regex=False)

if C["utilization_pct"] and C["utilization_pct"] in df.columns:
    u = to_num(df[C["utilization_pct"]])
    df["% ניצול תקציב - מחושב"] = u * 100 if u.max() <= 1.5 and u.max() > 0 else u
elif C["budget"] and C["utilization_total"]:
    df["% ניצול תקציב - מחושב"] = np.where(
        to_num(df[C["budget"]]) > 0,
        to_num(df[C["utilization_total"]]) / to_num(df[C["budget"]]) * 100,
        0,
    )
else:
    df["% ניצול תקציב - מחושב"] = 0

df["סטטוס ניצול תקציב - מחושב"] = df["% ניצול תקציב - מחושב"].apply(budget_status)

if C["expected_participants"] and C["actual_participants"]:
    df["% גיוס משתתפים"] = np.where(
        to_num(df[C["expected_participants"]]) > 0,
        to_num(df[C["actual_participants"]]) / to_num(df[C["expected_participants"]]) * 100,
        0,
    )
else:
    df["% גיוס משתתפים"] = 0

df["סטטוס גיוס"] = df["% גיוס משתתפים"].apply(recruitment_status)
df["ימים לסיום"] = (df[C["end_date"]] - pd.Timestamp.today().normalize()).dt.days if C["end_date"] else np.nan

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
    C["expected_income"], C["actual_income"], "שיעור מימוש הכנסות", C["total_expenses"],
    C["expected_participants"], C["actual_participants"], "% גיוס משתתפים",
    "% ניצול תקציב - מחושב", "סטטוס ניצול תקציב - מחושב", "רמזור ניהולי",
]

budget_cols = [
    C["study_id"], C["protocol"], C["pi"], C["department"], C["sponsor"],
    C["funding_type"], "קבוצת מימון", C["wbs"], C["budget_name"], C["budget"],
    C["utilization_total"], "% ניצול תקציב - מחושב", C["balance"],
    C["unreserved_balance"], C["end_date"], "ימים לסיום", "סטטוס גיוס",
    "סטטוס ניצול תקציב - מחושב", "רמזור ניהולי",
]

researcher_cols = [
    C["study_id"], C["protocol"], C["sponsor"], C["funding_type"], "קבוצת מימון",
    C["wbs"], C["budget_name"], C["budget"], "% ניצול תקציב - מחושב",
    C["balance"], "סטטוס ניצול תקציב - מחושב", "רמזור ניהולי",
]

identity_cols = [
    C["study_id"], C["protocol"], C["pi"], C["department"], C["site"], C["sponsor"],
    C["study_type"], C["funding_type"], "קבוצת מימון", C["phase"], C["start_date"],
    C["end_date"], C["budget_name"], C["budget_owner"], C["wbs"], C["contract"],
    C["budget"], C["execution"], C["commitment"], C["utilization_total"], C["balance"],
    C["unreserved_balance"], "% ניצול תקציב - מחושב", C["expected_income"],
    C["actual_income"], "שיעור מימוש הכנסות", C["expected_participants"],
    C["actual_participants"], "% גיוס משתתפים", "סטטוס גיוס", "רמזור ניהולי",
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

    kpis(
        [
            (first_label, first_val if first_val is not None else number(count_studies(data, C["unique_study"], C["study_id"]))),
            ("צפי הכנסות", money(exp)),
            ("הכנסות בפועל", money(act)),
            ("מימוש הכנסות", pct(real)),
        ],
        columns_per_row=4,
    )


# ============================================================
# PAGES
# ============================================================

if page == "📌 תקציר מנהלים":
    page_header("📌 תקציר מנהלים", "תמונת מצב מרוכזת להנהלה: מחקרים, הכנסות, הוצאות, מימון, תקציב וגיוס.")
    explain()
    common_kpis(df)
    render_insights("תובנות מרכזיות", insights(df, C))

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


elif page == "🏥 כלל בית החולים":
    page_header("🏥 כלל בית החולים", "ניתוח רוחבי של כלל המחקרים לפי שנים, מימון, הכנסות, הוצאות וחוקרים מובילים.")
    explain()
    d = df.copy()

    with st.container(border=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            d = filter_multi(d, "שנה", C["approval_year"], "h_y")
        with f2:
            d = filter_multi(d, "קבוצת מימון", "קבוצת מימון", "h_f")
        with f3:
            d = filter_multi(d, "סוג מחקר", C["study_type"], "h_t")

    common_kpis(d)
    render_insights("תובנות כלל בית החולים", insights(d, C))

    if C["approval_year"]:
        if C["unique_study"]:
            s = d.groupby(C["approval_year"], as_index=False)[C["unique_study"]].sum().rename(columns={C["approval_year"]: "שנה", C["unique_study"]: "מספר מחקרים"})
        else:
            s = d.groupby(C["approval_year"], as_index=False).size().rename(columns={C["approval_year"]: "שנה", "size": "מספר מחקרים"})
        chart_start(); bar(s, "שנה", "מספר מחקרים", "סה״כ מחקרים לפי שנה"); chart_end()

        ycols = [x for x in [C["expected_income"], C["actual_income"], C["total_expenses"], C["overhead"]] if x]
        if ycols:
            ym = d.groupby(C["approval_year"], as_index=False)[ycols].sum().rename(columns={C["approval_year"]: "שנה"})
            chart_start(); grouped(ym, "שנה", ycols, "צפי הכנסות, הכנסות בפועל, הוצאות ותקורה לפי שנה"); chart_end()

        chart_start(); plot_realization_year(d, C["approval_year"], C["expected_income"], C["actual_income"]); chart_end()

    c1, c2 = st.columns(2)
    with c1:
        chart_start(); funding_chart(d, C["unique_study"]); chart_end()
    with c2:
        if C["funding_type"] and C["unique_study"]:
            s = d.groupby(C["funding_type"], as_index=False)[C["unique_study"]].sum().rename(columns={C["funding_type"]: "סוג מימון", C["unique_study"]: "מספר מחקרים"})
            chart_start(); donut(s, "סוג מימון", "מספר מחקרים", "התפלגות מחקרים לפי סוג מימון מפורט"); chart_end()

    c3, c4 = st.columns(2)
    with c3:
        if C["pi"] and C["unique_study"]:
            s = d.groupby(C["pi"], as_index=False)[C["unique_study"]].sum().rename(columns={C["pi"]: "חוקר ראשי", C["unique_study"]: "מספר מחקרים"})
            chart_start(); top10(s, "חוקר ראשי", "מספר מחקרים", "Top 10 חוקרים לפי כמות מחקרים"); chart_end()
    with c4:
        if C["pi"] and C["expected_income"]:
            s = d.groupby(C["pi"], as_index=False)[C["expected_income"]].sum().rename(columns={C["pi"]: "חוקר ראשי", C["expected_income"]: "צפי הכנסות"})
            chart_start(); top10(s, "חוקר ראשי", "צפי הכנסות", "Top 10 חוקרים לפי צפי הכנסות"); chart_end()


elif page == "🏢 מחלקות":
    page_header("🏢 מחלקות", "דוח מחלקתי ממוקד: מחקרים, מימון, הכנסות, הוצאות, תקציב וגיוס לפי מחלקה.")
    explain()
    d = df.copy()

    with st.container(border=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            d, selected_department = filter_select(d, "מחלקה", C["department"], "d_sel")
        with f2:
            d = filter_multi(d, "שנה", C["approval_year"], "d_y")
        with f3:
            d = filter_multi(d, "קבוצת מימון", "קבוצת מימון", "d_f")

    common_kpis(d, "מחלקה", selected_department or "-")
    render_insights("תובנות מחלקה", insights(d, C))

    c1, c2 = st.columns(2)
    with c1:
        chart_start(); funding_chart(d, C["unique_study"]); chart_end()
    with c2:
        chart_start(); plot_realization_year(d, C["approval_year"], C["expected_income"], C["actual_income"]); chart_end()

    if C["approval_year"]:
        y = [x for x in [C["expected_income"], C["actual_income"], C["total_expenses"]] if x]
        if y:
            s = d.groupby(C["approval_year"], as_index=False)[y].sum().rename(columns={C["approval_year"]: "שנה"})
            chart_start(); grouped(s, "שנה", y, "הכנסות והוצאות לפי שנה במחלקה"); chart_end()

    render_table(d, "טבלת מחקרים במחלקה", study_cols, money_cols, pct_cols, num_cols2, date_cols)
    st.download_button("⬇️ הורדת דוח מחלקה לאקסל", download_excel({"department_report": d}), "department_report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


elif page == "👩‍⚕️ חוקרים":
    page_header("👩‍⚕️ חוקרים", "ניתוח לפי חוקר ראשי: הפרדה בין מחקרי יזם וגרנט, הכנסות, הוצאות, תקציב וגיוס.")
    explain()
    d = df.copy()

    with st.container(border=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            d, selected_pi = filter_select(d, "חוקר ראשי", C["pi"], "p_sel")
        with f2:
            d = filter_multi(d, "שנה", C["approval_year"], "p_y")
        with f3:
            d = filter_multi(d, "קבוצת מימון", "קבוצת מימון", "p_f")

    common_kpis(d, "חוקר", selected_pi or "-")
    render_insights("תובנות חוקר", insights(d, C))

    c1, c2 = st.columns(2)
    with c1:
        chart_start(); funding_chart(d, C["unique_study"]); chart_end()
    with c2:
        chart_start(); expense_chart(d, expense_map, "התפלגות הוצאות לחוקר"); chart_end()

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


elif page == "🏭 יזמים":
    page_header("🏭 יזמים", "ניתוח לפי יזם: כמות מחקרים, צפי הכנסות, הכנסות בפועל והוצאות.")
    d = df.copy()

    with st.container(border=True):
        f1, f2 = st.columns(2)
        with f1:
            d = filter_multi(d, "יזם", C["sponsor"], "s_s")
        with f2:
            d = filter_multi(d, "שנה", C["approval_year"], "s_y")

    if C["sponsor"]:
        s = d.groupby(C["sponsor"], as_index=False).size().rename(columns={C["sponsor"]: "יזם", "size": "מספר רשומות"})

        if C["unique_study"]:
            count_df = d.groupby(C["sponsor"], as_index=False)[C["unique_study"]].sum().rename(columns={C["sponsor"]: "יזם", C["unique_study"]: "מספר מחקרים"})
            s = s.merge(count_df, on="יזם", how="left")
        else:
            s["מספר מחקרים"] = s["מספר רשומות"]

        for col, name in [(C["expected_income"], "צפי הכנסות"), (C["actual_income"], "הכנסות בפועל"), (C["total_expenses"], "סך הוצאות")]:
            if col:
                temp = d.groupby(C["sponsor"], as_index=False)[col].sum().rename(columns={C["sponsor"]: "יזם", col: name})
                s = s.merge(temp, on="יזם", how="left")

        s = s.sort_values("מספר מחקרים", ascending=False)
        real = s["הכנסות בפועל"].sum() / s["צפי הכנסות"].sum() * 100 if "הכנסות בפועל" in s.columns and "צפי הכנסות" in s.columns and s["צפי הכנסות"].sum() > 0 else 0

        kpis([
            ("מספר יזמים", number(s["יזם"].nunique())),
            ("סה״כ מחקרים", number(s["מספר מחקרים"].sum())),
            ("צפי הכנסות", money(s.get("צפי הכנסות", pd.Series([0])).sum())),
            ("מימוש הכנסות", pct(real)),
        ])

        c1, c2 = st.columns(2)
        with c1:
            chart_start(); top10(s, "יזם", "מספר מחקרים", "Top 10 יזמים לפי כמות מחקרים"); chart_end()
        with c2:
            if "צפי הכנסות" in s.columns:
                chart_start(); top10(s, "יזם", "צפי הכנסות", "Top 10 יזמים לפי צפי הכנסות"); chart_end()

        render_table(s, "טבלת סיכום יזמים", money_cols=["צפי הכנסות", "הכנסות בפועל", "סך הוצאות"], num_cols=["מספר רשומות", "מספר מחקרים"])


elif page == "🚦 בקרת תקציב וגיוס":
    page_header("🚦 בקרת תקציב וגיוס", "דוח בדיקה ניהולי: חריגות תקציב, ניצול נמוך, גיוס נמוך, סיום קרוב ורמזור ניהולי.")
    explain()
    d = df.copy()

    with st.container(border=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            d = filter_multi(d, "שנה", C["approval_year"], "t_y")
        with f2:
            d = filter_multi(d, "מחלקה", C["department"], "t_d")
        with f3:
            d = filter_multi(d, "חוקר ראשי", C["pi"], "t_p")
        f4, f5, f6 = st.columns(3)
        with f4:
            d = filter_multi(d, "קבוצת מימון", "קבוצת מימון", "t_f")
        with f5:
            d = filter_multi(d, "סטטוס ניצול", "סטטוס ניצול תקציב - מחושב", "t_u")
        with f6:
            d = filter_multi(d, "סטטוס גיוס", "סטטוס גיוס", "t_r")

    over = d[d["סטטוס ניצול תקציב - מחושב"] == "חריגה"]
    high = d[d["סטטוס ניצול תקציב - מחושב"] == "קרוב לניצול מלא"]
    low = d[d["סטטוס ניצול תקציב - מחושב"] == "ניצול נמוך"]
    lowrec = d[d["סטטוס גיוס"].isin(["אין גיוס", "גיוס נמוך"])]
    soon = d[(d["ימים לסיום"] >= 0) & (d["ימים לסיום"] <= 60)]

    kpis([
        ("🔴 חריגה תקציבית", number(len(over))),
        ("🟡 קרוב לניצול מלא", number(len(high))),
        ("🟡 ניצול נמוך", number(len(low))),
        ("🟡 גיוס נמוך / אין גיוס", number(len(lowrec))),
    ])

    c1, c2 = st.columns(2)
    with c1:
        s = d.groupby("סטטוס ניצול תקציב - מחושב", as_index=False).size().rename(columns={"size": "מספר מחקרים"})
        chart_start(); donut(s, "סטטוס ניצול תקציב - מחושב", "מספר מחקרים", "התפלגות סטטוס ניצול תקציבי"); chart_end()
    with c2:
        s = d.groupby("סטטוס גיוס", as_index=False).size().rename(columns={"size": "מספר מחקרים"})
        chart_start(); donut(s, "סטטוס גיוס", "מספר מחקרים", "התפלגות סטטוס גיוס"); chart_end()

    choice = st.radio("בחרי סוג בדיקה להצגה", ["🔴 חריגה תקציבית", "🟡 קרוב לניצול מלא", "🟡 ניצול נמוך", "🟡 גיוס נמוך", "🟡 סיום קרוב", "📋 כל הסטטוסים"], horizontal=True)

    if choice == "🔴 חריגה תקציבית":
        table, title = over, "מחקרים בחריגה תקציבית"
    elif choice == "🟡 קרוב לניצול מלא":
        table, title = high, "מחקרים קרובים לניצול מלא"
    elif choice == "🟡 ניצול נמוך":
        table, title = low, "מחקרים בניצול נמוך"
    elif choice == "🟡 גיוס נמוך":
        table, title = lowrec, "מחקרים עם גיוס נמוך / ללא גיוס"
    elif choice == "🟡 סיום קרוב":
        table, title = soon, "מחקרים שמסתיימים תוך 60 יום"
    else:
        table, title = d, "טבלת בקרת תקציב וגיוס"

    render_table(table, title, budget_cols, money_cols, pct_cols, num_cols2, date_cols)
    st.download_button("⬇️ הורדת דוח בקרת תקציב וגיוס לאקסל", download_excel({"budget_recruitment_report": d}), "budget_recruitment_report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


elif page == "🧾 דוח חוקר":
    page_header("🧾 דוח חוקר", "בחירת חוקר ומחקר ספציפי לצורך צפייה בתעודת זהות ניהולית, תקציב, ביצוע והוצאות.")
    explain()
    d = df.copy()

    with st.container(border=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            d, selected_researcher = filter_select(d, "בחירת חוקר", C["pi"], "r_sel")
        with f2:
            d = filter_multi(d, "שנה", C["approval_year"], "r_y")
        with f3:
            d = filter_multi(d, "קבוצת מימון", "קבוצת מימון", "r_f")

    if d.empty:
        st.info("אין מחקרים להצגה עבור הבחירה הנוכחית.")
        st.stop()

    exp = sum_col(d, C["expected_income"])
    act = sum_col(d, C["actual_income"])

    kpis([
        ("חוקר", selected_researcher or "-"),
        ("מספר מחקרים", number(count_studies(d, C["unique_study"], C["study_id"]))),
        ("תקציב כולל", money(sum_col(d, C["budget"]))),
        ("מימוש הכנסות", pct(act / exp * 100 if exp > 0 else 0)),
    ])

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
        selected_display = st.selectbox("בחרי מחקר ספציפי", study_options, key="researcher_specific_study")
        selected_study_key = selected_display.split(" | ")[0].strip()
        one = d[d[C["study_id"]].apply(clean_key) == selected_study_key]
    else:
        st.warning("לא נמצאה עמודת מספר הלסינקי ולכן לא ניתן לפתוח תעודת זהות למחקר.")
        one = pd.DataFrame()

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

        html = '<div class="identity-grid">'
        for label, value in cards:
            html += f"""
            <div class="identity-card">
                <div class="identity-label">{label}</div>
                <div class="identity-value">{value}</div>
            </div>
            """
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

        pay = payment_for(details, one, C, D, selected_researcher)
        c1, c2 = st.columns(2)
        with c1:
            chart_start(); budget_exec_chart(pay, D); chart_end()
        with c2:
            chart_start(); expense_chart(one, expense_map, f"התפלגות הוצאות למחקר {selected_study_key}"); chart_end()

        render_table(one, "פרטים מלאים למחקר שנבחר", identity_cols, money_cols, pct_cols, num_cols2, date_cols, 330)
        if pay is not None and not pay.empty:
            render_table(pay, "פירוט תקציבי מתוך מעקב דרישות תשלום", payment_cols, money_cols, pct_cols, num_cols2, date_cols, 330)

        st.download_button(
            "⬇️ הורדת דוח המחקר שנבחר לאקסל",
            download_excel({"study_identity": one, "payment_details": pay if pay is not None else pd.DataFrame()}),
            f"study_{selected_study_key}_report.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


elif page == "💳 מעקב דרישות תשלום":
    page_header("💳 מעקב דרישות תשלום", "מעקב תקציבי לפי חוקר/מחקר: תקציב, התחייבויות, ביצוע, יתרה ופירוט לפי קטגוריות.")
    source = df.copy()

    with st.container(border=True):
        source, selected_researcher = filter_select(source, "חוקר", C["pi"], "pay_sel")

    pay = payment_for(details, source, C, D, selected_researcher)

    if D["study_id"] and D["study_id"] in pay.columns and not pay.empty:
        pay = filter_multi(pay, "מחקר", D["study_id"], "pay_study")

    kpis([
        ("חוקר", selected_researcher or "-"),
        ("סה״כ תקציב", money(sum_col(pay, D["budget_total"]))),
        ("התחייבויות רכש", money(sum_col(pay, D["purchase_commitments"]))),
        ("סה״כ ביצוע", money(sum_col(pay, D["execution_total"]))),
    ])

    chart_start(); budget_exec_chart(pay, D); chart_end()

    if D["budget_category"] and D["budget_category"] in pay.columns:
        y = [D["budget_total"], D["purchase_commitments"], D["execution_total"], D["balance"]]
        y = [x for x in y if x and x in pay.columns]
        if y:
            cat = pay.groupby(D["budget_category"], as_index=False)[y].sum().rename(columns={D["budget_category"]: "קטגוריית סעיף תקציבי"})
            c1, c2 = st.columns(2)
            with c1:
                render_table(cat, "סיכום לפי קטגוריית סעיף תקציבי", money_cols=y, height=310)
            with c2:
                chart_start(); grouped(cat, "קטגוריית סעיף תקציבי", y, "תקציב, התחייבויות, ביצוע ויתרה לפי קטגוריה", 360); chart_end()

    if D["wbs"] and D["wbs"] in pay.columns:
        y = [D["budget_total"], D["purchase_commitments"], D["execution_total"], D["balance"]]
        y = [x for x in y if x and x in pay.columns]
        if y:
            wbs_summary = pay.groupby(D["wbs"], as_index=False)[y].sum().rename(columns={D["wbs"]: "אלמנט WBS"})
            render_table(wbs_summary, "סיכום לפי WBS", money_cols=y, height=300)

    render_table(pay, "טבלת מעקב דרישות תשלום", payment_cols, money_cols, pct_cols, num_cols2, date_cols)
    st.download_button(
        "⬇️ הורדת מעקב דרישות תשלום לאקסל",
        download_excel({"payment_tracking": pay}),
        "researcher_payment_tracking.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
