import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ============================================================
# הגדרות עמוד
# ============================================================
st.set_page_config(
    page_title="דשבורד מחקרים קליניים",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# עיצוב RTL ויישור טבלאות לימין
# ============================================================
st.markdown(
    """
    <style>
    /* הגדרות כיווניות ויישור טקסט כללי */
    html, body, [class*="css"], .stApp {
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

    /* אילוץ יישור לימין (RTL) עבור טבלאות הנתונים של Streamlit */
    div[data-testid="stDataFrame"] div {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* עיצוב כרטיסי ה-KPI */
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
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# פונקציות עזר ובעיות תאימות עמודות
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

# ============================================================
# פונקציות גרפים
# ============================================================
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

# ============================================================
# כותרת והעלאת קובץ
# ============================================================
st.title("📊 דשבורד ניהולי למחקרים קליניים")

uploaded_file = st.file_uploader("העלי קובץ Excel להפעלת הדשבורד", type=["xlsx"])

if uploaded_file is None:
    st.markdown(
        """
        <div class="info-box">
        ברוכה הבאה! אנא העלי קובץ Excel הכולל את הגיליונות הקבועים כדי לפתוח את הדשבורד האוטומטי.
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.stop()

# קריאת קובץ האקסל וטעינה אוטומטית לפי שמות הגיליונות הקבועים
try:
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names
    
    # חיפוש אוטומטי של הגיליונות ללא בחירה ידנית
    studies_sheet = None
    details_sheet = None
    
    for s in sheet_names:
        norm_s = normalize_text(s).lower()
        if "studies" in norm_s or "מחקרים" in norm_s:
            studies_sheet = s
        elif "פירוט" in norm_s or "הוצאות" in norm_s or "details" in norm_s:
            details_sheet = s
            
    # לוגיקת גיבוי (Fallback) אם השמות לא נמצאו בדיוק
    if not studies_sheet:
        studies_sheet = sheet_names[0]
    if not details_sheet:
        details_sheet = sheet_names[1] if len(sheet_names) > 1 else sheet_names[0]
    
    studies_df = normalize_columns(pd.read_excel(uploaded_file, sheet_name=studies_sheet))
    details_df = normalize_columns(pd.read_excel(uploaded_file, sheet_name=details_sheet))
    
except Exception as e:
    st.error("שגיאה בטעינת הנתונים מהקובץ. ודאי שהגיליונות קיימים.")
    st.write(e)
    st.stop()

# ============================================================
# מיפוי עמודות אוטומטי
# ============================================================
C = {
    "approval_date": find_col(studies_df, ["תאריך אישור מחקר"]),
    "approval_year": find_col(studies_df, ["שנת אישור המחקר", "שנת אישור מחקר"]),
    "start_date": find_col(studies_df, ["תאריך תחילה"]),
    "end_date": find_col(studies_df, ["תאריך סיום"]),
    "protocol": find_col(studies_df, ["סימון פרוטוקול", "מספר פרוטוקול"]),
    "study_id": find_col(studies_df, ["סוג תכנית-study_id", "סוג תכנית – study_id", "סוג תכנית - study_id", "מספר הלסינקי"]),
    "pi": find_col(studies_df, ["חוקר ראשי", "שם חוקר ראשי"]),
    "department": find_col(studies_df, ["מחלקה"]),
    "study_type": find_col(studies_df, ["סוג המחקר"]),
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
    "budget": find_col(studies_df, ["תקציב"]),
    "overhead": find_col(studies_df, ["תקורה לפי 18%", "תקורה"]),
    "balance": find_col(studies_df, ["יתרה לניצול"]),
    "utilization_pct": find_col(studies_df, ["% ניצול תקציב", "אחוז ניצול תקציב"]),
}

# ניקוי המרה נומרית
numeric_cols = [c for c in C.values() if c in studies_df.columns]
studies_df = make_numeric(studies_df, [c for c in numeric_cols if c])

if C["approval_date"] and C["approval_date"] in studies_df.columns:
    studies_df[C["approval_date"]] = to_date(studies_df[C["approval_date"]])
    if C["approval_year"] is None:
        studies_df["שנת אישור המחקר - מחושב"] = studies_df[C["approval_date"]].dt.year
        C["approval_year"] = "שנת אישור המחקר - מחושב"

if C["utilization_pct"]:
    util = to_numeric(studies_df[C["utilization_pct"]])
    if util.max() <= 1.5 and util.max() > 0:
        util = util * 100
    studies_df["% ניצול תקציב - מחושב"] = util
else:
    studies_df["% ניצול תקציב - מחושב"] = 0

studies_df["סטטוס ניצול תקציב - מחושב"] = studies_df["% ניצול תקציב - מחושב"].apply(budget_status)

if C["expected_participants"] and C["actual_participants"]:
    expected = to_numeric(studies_df[C["expected_participants"]])
    actual = to_numeric(studies_df[C["actual_participants"]])
    studies_df["% גיוס משתתפים"] = np.where(expected > 0, actual / expected * 100, 0)
else:
    studies_df["% גיוס משתתפים"] = 0

studies_df["רמזור ניהולי"] = studies_df.apply(
    lambda row: traffic_light(
        row["סטטוס ניצול תקציב - מחושב"],
        row[C["balance"]] if C["balance"] else None,
        np.nan,
        row["% גיוס משתתפים"]
    ),
    axis=1
)

# ============================================================
# יצירת מבנה הטאבים (הפרדה מלאה)
# ============================================================
tabs = st.tabs([
    "🏥 כלל בית החולים",
    "🏢 מחלקות",
    "👩‍⚕️ חוקרים",
    "🏭 יזמים",
    "🚦 סטטוס ניהול תקציב"
])

# ------------------------------------------------------------
# הטאב הראשון: כלל בית החולים (כולל KPIs ומידע כללי)
# ------------------------------------------------------------
with tabs[0]:
    st.header("🏥 סקירה כללית - כלל בית החולים")
    
    # פילטרים מקומיים בלבד
    c1, c2 = st.columns(2)
    with c1:
        years_list = sorted(studies_df[C["approval_year"]].dropna().astype(str).unique()) if C["approval_year"] else []
        selected_years = st.multiselect("סנני לפי שנת אישור (בי''ח)", years_list, default=years_list)
    with c2:
        funding_list = sorted(studies_df[C["funding_type"]].dropna().astype(str).unique()) if C["funding_type"] else []
        selected_funding = st.multiselect("סנני לפי סוג מימון (בי''ח)", funding_list, default=funding_list)
        
    hospital_df = studies_df.copy()
    if selected_years and C["approval_year"]:
        hospital_df = hospital_df[hospital_df[C["approval_year"]].astype(str).isin(selected_years)]
    if selected_funding and C["funding_type"]:
        hospital_df = hospital_df[hospital_df[C["funding_type"]].astype(str).isin(selected_funding)]

    # כרטיסי המידע הכללי מופיעים אך ורק כאן
    st.markdown("### מדדי מפתח בית חולימיים")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("סה״כ מחקרים", number(count_unique_studies(hospital_df, C["unique_study"], C["study_id"])))
    k2.metric("מספר חוקרים", number(hospital_df[C["pi"]].nunique() if C["pi"] else 0))
    k3.metric("מספר מחלקות", number(hospital_df[C["department"]].nunique() if C["department"] else 0))
    k4.metric("מספר יזמים", number(hospital_df[C["sponsor"]].nunique() if C["sponsor"] else 0))

    k5, k6, k7, k8 = st.columns(4)
    k5.metric("צפי הכנסות", money(sum_col(hospital_df, C["expected_income"])))
    k6.metric("הכנסות בפועל", money(sum_col(hospital_df, C["actual_income"])))
    k7.metric("סך הוצאות", money(sum_col(hospital_df, C["total_expenses"])))
    k8.metric("תקורה", money(sum_col(hospital_df, C["overhead"])))

    if C["approval_year"]:
        yearly = hospital_df.groupby(C["approval_year"], as_index=False).size().rename(columns={"size": "מספר מחקרים"})
        plot_bar(yearly, C["approval_year"], "מספר מחקרים", "סה״כ מחקרים לפי שנה")

    st.subheader("כלל הנתונים")
    st.dataframe(hospital_df, use_container_width=True)

# ------------------------------------------------------------
# הטאב השני: מחלקות (פילטר מחלקה ושנה)
# ------------------------------------------------------------
with tabs[1]:
    st.header("🏢 ניתוח ברמת מחלקות")
    
    if C["department"]:
        f1, f2 = st.columns(2)
        with f1:
            all_depts = sorted(studies_df[C["department"]].dropna().astype(str).unique())
            selected_dept = st.selectbox("בחרי מחלקה למיקוד", all_depts)
        with f2:
            sub_df = studies_df[studies_df[C["department"]].astype(str) == selected_dept]
            dept_years = sorted(sub_df[C["approval_year"]].dropna().astype(str).unique()) if C["approval_year"] else []
            selected_dept_years = st.multiselect("בחרי שנה / שנים", dept_years, default=dept_years)
            
        dept_df = studies_df[studies_df[C["department"]].astype(str) == selected_dept]
        if selected_dept_years and C["approval_year"]:
            dept_df = dept_df[dept_df[C["approval_year"]].astype(str).isin(selected_dept_years)]
            
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("מספר מחקרים במחלקה", number(count_unique_studies(dept_df, C["unique_study"], C["study_id"])))
        d2.metric("צפי הכנסות", money(sum_col(dept_df, C["expected_income"])))
        d3.metric("הכנסות בפועל", money(sum_col(dept_df, C["actual_income"])))
        d4.metric("סך הוצאות", money(sum_col(dept_df, C["total_expenses"])))
        
        st.subheader(f"טבלת מחקרים ממוקדת - מחלקת {selected_dept}")
        st.dataframe(dept_df, use_container_width=True)
    else:
        st.warning("עמודת מחלקה לא זוהתה בקובץ.")

# ------------------------------------------------------------
# הטאב השלישי: חוקרים (פילטר חוקר ושנה)
# ------------------------------------------------------------
with tabs[2]:
    st.header("👩‍⚕️ ניתוח לפי חוקר ראשי")
    
    if C["pi"]:
        f1, f2 = st.columns(2)
        with f1:
            all_pis = sorted(studies_df[C["pi"]].dropna().astype(str).unique())
            selected_pi = st.selectbox("בחרי חוקר ראשי", all_pis)
        with f2:
            sub_pi = studies_df[studies_df[C["pi"]].astype(str) == selected_pi]
            pi_years = sorted(sub_pi[C["approval_year"]].dropna().astype(str).unique()) if C["approval_year"] else []
            selected_pi_years = st.multiselect("בחרי שנה / שנים לחוקר זה", pi_years, default=pi_years)
            
        pi_df = studies_df[studies_df[C["pi"]].astype(str) == selected_pi]
        if selected_pi_years and C["approval_year"]:
            pi_df = pi_df[pi_df[C["approval_year"]].astype(str).isin(selected_pi_years)]
            
        p1, p2, p3, p4 = st.columns(4)
        p1.metric("מחקרים לחוקר", number(count_unique_studies(pi_df, C["unique_study"], C["study_id"])))
        p2.metric("צפי הכנסות", money(sum_col(pi_df, C["expected_income"])))
        p3.metric("הכנסות בפועל", money(sum_col(pi_df, C["actual_income"])))
        p4.metric("סך הוצאות", money(sum_col(pi_df, C["total_expenses"])))
        
        st.subheader("טבלת מחקרים המשויכים לחוקר")
        st.dataframe(pi_df, use_container_width=True)
    else:
        st.warning("עמודת חוקר ראשי לא זוהתה.")

# ------------------------------------------------------------
# הטאב הרביעי: יזמים (פילטר יזמים מרובה)
# ------------------------------------------------------------
with tabs[3]:
    st.header("🏭 ניתוח לפי גורמים מממנים ויזמים")
    
    if C["sponsor"]:
        all_sponsors = sorted(studies_df[C["sponsor"]].dropna().astype(str).unique())
        selected_sponsors = st.multiselect("בחרי יזמים להצגה", all_sponsors, default=all_sponsors[:5] if len(all_sponsors) > 5 else all_sponsors)
        
        sponsor_df = studies_df[studies_df[C["sponsor"]].astype(str).isin(selected_sponsors)]
        
        if not sponsor_df.empty:
            sponsor_count = sponsor_df.groupby(C["sponsor"], as_index=False).size().rename(columns={"size": "מספר מחקרים"})
            plot_pie(sponsor_count, C["sponsor"], "מספר מחקרים", "התפלגות מחקרים בין היזמים הנבחרים")
            
        st.subheader("טבלת נתונים מפורטת לפי יזם")
        st.dataframe(sponsor_df, use_container_width=True)

# ------------------------------------------------------------
# הטאב החמישי: סטטוס ניהול תקציב
# ------------------------------------------------------------
with tabs[4]:
    st.header("🚦 סטטוס ניצול תקציב ומערכת רמזורים")
    
    status_summary = studies_df.groupby("סטטוס ניצול תקציב - מחושב", as_index=False).size().rename(columns={"size": "מספר מחקרים"})
    plot_bar(status_summary, "סטטוס ניצול תקציב - מחושב", "מספר מחקרים", "סטטוס ניצול תקציבי של כלל המחקרים")
    
    traffic_summary = studies_df.groupby("רמזור ניהולי", as_index=False).size().rename(columns={"size": "מספר מחקרים"})
    plot_bar(traffic_summary, "רמזור ניהולי", "מספר מחקרים", "פילוח רמזור ניהולי")
    
    st.subheader("מחקרים בסטטוס חריגה או סיכון תקציבי/גיוסי (רמזור אדום וצהוב)")
    risk_df = studies_df[studies_df["רמזור ניהולי"].str.contains("אדום|צהוב", na=False)]
    st.dataframe(risk_df, use_container_width=True)
