import streamlit as st
import pandas as pd

st.set_page_config(page_title="Restricted CSV Viewer", layout="wide")
st.title("📤 CSV Upload + 🔒 LGA-Restricted Access")

# 🔐 Define user access (name or email → allowed LGA)
user_access = {
    "alice@gmail.com": "Kaduna North",
    "bob@yahoo.com": "Kaduna South",
    "charlie@outlook.com": "Chikun",
    "danjuma@gmail.com": "Kaduna North",
}

# 📤 Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        if "Email" not in df.columns or "LGA" not in df.columns:
            st.error("❌ Your CSV must contain at least 'Email' and 'LGA' columns.")
        else:
            user_email = st.text_input("Enter your email to access your LGA data:")

            if user_email:
                if user_email in user_access:
                    allowed_lga = user_access[user_email]
                    st.success(f"✅ Access granted! Showing data for LGA: **{allowed_lga}**")

                    filtered_df = df[df["LGA"] == allowed_lga]
                    st.dataframe(filtered_df)

                    csv = filtered_df.to_csv(index=False).encode("utf-8")
                    st.download_button("Download filtered data", data=csv, file_name=f"{allowed_lga}_data.csv", mime="text/csv")
                else:
                    st.error("❌ You are not authorized to view this data.")
            else:
                st.info("👈 Enter your email to filter by your assigned LGA.")
    except Exception as e:
        st.error(f"⚠️ Error reading CSV: {e}")
else:
    st.info("📥 Upload a CSV file to begin.")
