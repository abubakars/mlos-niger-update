import streamlit as st
import pandas as pd
import requests
from io import StringIO
from datetime import datetime

st.markdown("<h1 style='text-align: center;'>Niger MLoS</h1>", unsafe_allow_html=True)

# --- Load from GitHub ---
raw_url = "https://raw.githubusercontent.com/abubakars/mlos-niger-update/refs/heads/main/MLOSS.csv"
resp = requests.get(raw_url)
if resp.status_code == 200:
    df = pd.read_csv(StringIO(resp.text))
else:
    st.error("❌ Failed to load data from GitHub")
    st.stop()

# --- Sidebar form to add data ---
st.sidebar.markdown("### ➕ Add New Entry")

with st.sidebar.form("add_data_form"):
    name = st.text_input("Name")
    region = st.selectbox("Region", ["North", "South", "East", "West"])  # adapt to your CSV
    project = st.text_input("Project")
    date = st.date_input("Date", format="DD/MM/YYYY")
    submitted = st.form_submit_button("Add Entry")

if submitted:
    new_row = {
        "Name": name,
        "Region": region,
        "Project": project,
        "Date": date.strftime("%d/%m/%Y")
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    st.success("✅ New entry added!")

# --- Filter section (after data is loaded and optionally updated) ---
st.markdown("### 🔍 Filter by LGA and Ward")

# Ensure columns exist before filtering
if "lga_name" in df.columns and "ward_name" in df.columns:
    lga_list = sorted(df["lga_name"].dropna().unique().tolist())
    ward_list = sorted(df["ward_name"].dropna().unique().tolist())

    col1, col2 = st.columns(2)
    with col1:
        selected_lga = st.selectbox("Select LGA", options=["All"] + lga_list)
    with col2:
        selected_ward = st.selectbox("Select Ward", options=["All"] + ward_list)

    filtered_df = df.copy()
    if selected_lga != "All":
        filtered_df = filtered_df[filtered_df["lga_name"] == selected_lga]
    if selected_ward != "All":
        filtered_df = filtered_df[filtered_df["ward_name"] == selected_ward]
else:
    st.warning("⚠️ Columns 'lga_name' and/or 'ward_name' are missing in the dataset.")
    filtered_df = df

# --- Display final filtered data ---
st.dataframe(filtered_df, use_container_width=True)

# --- Optional: Download filtered CSV ---
filtered_csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download filtered CSV", data=filtered_csv, file_name="filtered_MLOSS.csv", mime="text/csv")
