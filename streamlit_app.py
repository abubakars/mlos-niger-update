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
# TODO: Replace with your actual required columns!
columns_to_check = ['colA', 'colB', 'colC']  # <--- CHANGE THIS TO YOUR REQUIRED COLUMNS

def row_status(row):
    if any(pd.isna(row[col]) or row[col] == '' for col in columns_to_check):
        return '<span style="color:red; font-size:1.5em;">●</span>'
    else:
        return '<span style="color:green; font-size:1.5em;">●</span>'

# Don't mutate filtered_df in place before editing, use a copy for display
filtered_df_display = filtered_df.copy()
filtered_df_display['Status'] = filtered_df_display.apply(row_status, axis=1)

# --- Editable Table ---
st.markdown("### ✏️ Edit or Add Rows to the Table Below")

st.write("● = Status: Green = Complete, Red = Incomplete")
st.write(filtered_df_display.to_html(escape=False, index=False), unsafe_allow_html=True)

# Editable table (excluding Status column)
edited_df = st.data_editor(
    filtered_df,
    num_rows="dynamic",  # allow adding rows
    use_container_width=True,
    key="editable_table"
)

# --- Merge edits into full dataset ---
if not edited_df.equals(filtered_df):
    st.info("🔄 Updates detected: reflecting edits in the full table.")

    # Remove filtered rows from original df
    df_not_affected = df.copy()
    if selected_lga != "All":
        df_not_affected = df_not_affected[df_not_affected["lga_name"] != selected_lga]
    if selected_ward != "All":
        df_not_affected = df_not_affected[df_not_affected["ward_name"] != selected_ward]

    # Merge updated section back into main df
    df = pd.concat([df_not_affected, edited_df], ignore_index=True)

# --- Download edited/added data ---
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Full Updated CSV",
    data=csv,
    file_name="full_updated_MLOSS.csv",
    mime="text/csv"

# --- Expandable full table view ---
st.markdown("✅ Edits are applied. You can download or expand the full updated dataset below.")
with st.expander("📋 Show Full Updated Table"):
    # Recompute status for full df
    df_display = df.copy()
    df_display['Status'] = df_display.apply(row_status, axis=1)
    st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
