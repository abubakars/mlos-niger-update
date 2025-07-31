import streamlit as st
import pandas as pd

st.set_page_config(page_title="LGA Viewer from Google Sheets", layout="wide")
st.title("📄 View Google Sheet (Restricted by LGA)")

# 🔐 Define credentials (username → LGA)
credentials = {
    "abubakar": "Lapai",
    "name2": "Chikun",
    "name3": "Kaduna South",
}

# 🔗 Replace this with YOUR sheet export link
sheet_url = "https://docs.google.com/spreadsheets/d/1gja9oO9lhLlC8DQshOjPIkRbhFU2nrCE9Kuljs7-6vk/edit?gid=697693047#gid=697693047"

@st.cache_data
def load_data_from_gsheet(url):
    return pd.read_csv(url)

try:
    df = load_data_from_gsheet(sheet_url)

    if "LGA" not in df.columns:
        st.error("❌ Your Google Sheet must contain an 'LGA' column.")
    else:
        username = st.text_input("Enter your username (e.g. name1):")

        if username:
            if username in credentials:
                user_lga = credentials[username]
                st.success(f"✅ Access granted for LGA: **{user_lga}**")

                filtered_df = df[df["LGA"] == user_lga]
                st.subheader("📍 Your LGA Data")
                st.dataframe(filtered_df)

                # Optional: allow download
                csv = filtered_df.to_csv(index=False).encode("utf-8")
                st.download_button("Download your data", data=csv, file_name=f"{user_lga}_data.csv", mime="text/csv")
            else:
                st.error("❌ Invalid username.")
        else:
            st.info("👈 Enter your username to view data.")
except Exception as e:
    st.error(f"⚠️ Failed to load Google Sheet: {e}")
