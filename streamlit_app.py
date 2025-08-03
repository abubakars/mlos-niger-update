import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.set_page_config(page_title="Niger MLoS", layout="wide")

st.markdown("<h1 style='text-align: center;'>Niger MLoS</h1>", unsafe_allow_html=True)

# --- Load data from GitHub ---
raw_url = "https://raw.githubusercontent.com/abubakars/mlos-niger-update/refs/heads/main/MLoS_Niger.csv"
resp = requests.get(raw_url)
if resp.status_code == 200:
    df = pd.read_csv(StringIO(resp.text))
else:
    st.error("❌ Failed to load data from GitHub")
    st.stop()

# --- Filter by LGA and Ward ---
st.markdown("### 🔍 Filter by LGA and Ward")

if "lga_name" in df.columns and "ward_name" in df.columns:
    lga_list = sorted(df["lga_name"].dropna().unique())
    col1, col2 = st.columns(2)
    with col1:
        selected_lga = st.selectbox("Select LGA", ["All"] + lga_list)
    if selected_lga == "All":
        filtered_wards = sorted(df["ward_name"].dropna().unique())
    else:
        filtered_wards = sorted(df[df["lga_name"] == selected_lga]["ward_name"].dropna().unique())
    with col2:
        selected_ward = st.selectbox("Select Ward", ["All"] + filtered_wards)

    filtered_df = df.copy()
    if selected_lga != "All":
        filtered_df = filtered_df[filtered_df["lga_name"] == selected_lga]
    if selected_ward != "All":
        filtered_df = filtered_df[filtered_df["ward_name"] == selected_ward]
else:
    st.warning("⚠️ Columns 'lga_name' and/or 'ward_name' missing in data.")
    filtered_df = df.copy()

# --- Status Indicator Column ---
# ✅ Replace with real column names you want to check
columns_to_check = ['state_name', 'lga_name', 'ward_name', 'latitude', 'longitude']

def row_status(row):
    try:
        if any(pd.isna(row[col]) or str(row[col]).strip() == '' for col in columns_to_check):
            return '<span style="color:red; font-size:1.5em;">●</span>'
        else:
            return '<span style="color:green; font-size:1.5em;">●</span>'
    except KeyError:
        return '<span style="color:gray; font-size:1.5em;">●</span>'

filtered_df['Status'] = filtered_df.apply(row_status, axis=1)

# --- Editable Table ---
st.markdown("### ✏️ Edit or Add Rows to the Table Below")

st.write("● = Status: Green = Complete, Red = Incomplete")
st.write(filtered_df.to_html(escape=False), unsafe_allow_html=True)

edited_df = st.data_editor(
    filtered_df.drop(columns=['Status']),
    num_rows="dynamic",
    use_container_width=True,
    key="editable_table"
)

# --- Merge edits into full dataset ---
if not edited_df.equals(filtered_df.drop(columns=['Status'])):
    st.info("🔄 Updates detected: reflecting edits in the full table.")

    df_not_affected = df.copy()
    if selected_lga != "All":
        df_not_affected = df_not_affected[df_not_affected["lga_name"] != selected_lga]
    if selected_ward != "All":
        df_not_affected = df_not_affected[df_not_affected["ward_name"] != selected_ward]

    df = pd.concat([df_not_affected, edited_df], ignore_index=True)

# --- Download edited/added data ---
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Full Updated CSV",
    data=csv,
    file_name="full_updated_MLOSS.csv",
    mime="text/csv"
)

# --- Expandable full table view ---
st.markdown("✅ Edits are applied. You can download or expand the full updated dataset below.")
with st.expander("📋 Show Full Updated Table"):
    df['Status'] = df.apply(row_status, axis=1)
    st.write(df.to_html(escape=False), unsafe_allow_html=True)
