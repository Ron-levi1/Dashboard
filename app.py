
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="דשבורד מחקרים קליניים",
    page_icon="📊",
    layout="wide"
)

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: Arial, sans-serif;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 דשבורד מחקרים קליניים")
st.write("העלי קובץ Excel כדי להתחיל את הניתוח.")

uploaded_file = st.file_uploader("העלי קובץ Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        xls = pd.ExcelFile(uploaded_file)
        st.success("הקובץ נטען בהצלחה!")

        st.subheader("גיליונות שזוהו בקובץ")
        st.write(xls.sheet_names)

        selected_sheet = st.selectbox("בחרי גיליון להצגה", xls.sheet_names)

        df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
        df.columns = df.columns.astype(str).str.strip()

        st.subheader("תצוגה ראשונית של הנתונים")
        st.dataframe(df.head(50), use_container_width=True)

        st.subheader("מידע כללי")
        col1, col2, col3 = st.columns(3)
        col1.metric("מספר שורות", len(df))
        col2.metric("מספר עמודות", len(df.columns))
        col3.metric("מספר גיליונות", len(xls.sheet_names))

    except Exception as e:
        st.error("הייתה בעיה בקריאת קובץ האקסל.")
        st.write(e)

else:
    st.info("יש להעלות קובץ Excel כדי להתחיל.")
