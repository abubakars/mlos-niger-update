import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Viewer with LGA Filter", layout="wide")
st.title("📄 CSV Viewer with LGA Filter")

# 📤 Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        if "LGA" not in df.columns:
            st.error("❌ Your CSV must contain a column named 'LGA'.")
        else:
            st.success("✅ File loaded successfully.")

            # 🌐 Dropdown to filter by LGA
            unique_lgas = df["LGA"].dropna().unique()
            selected_lga = st.selectbox("Filter by LGA:", options=["All"] + sorted(unique_lgas.tolist()))

            if selected_lga == "All":
                filtered_df = df
            else:
                filtered_df = df[df["LGA"] == selected_lga]

            st.dataframe(filtered_df)

            # 📥 Download button
            csv = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button("Download filtered data", data=csv, file_name="filtered_data.csv", mime="text/csv")
    except Exception as e:
        st.error(f"⚠️ Error reading CSV: {e}")
else:
    st.info("📥 Upload a CSV file to begin.")
