import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Uploader", layout="wide")
st.title("📤 Upload and View CSV")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
        st.subheader("📄 CSV Preview")
        st.dataframe(df)
    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
else:
    st.info("👈 Upload a .csv file to get started.")
