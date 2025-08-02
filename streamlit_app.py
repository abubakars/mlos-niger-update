import streamlit as st
import pandas as pd
import requests
from io import StringIO
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(page_title="Niger MLoS", layout="wide")
st.markdown("<h1 style='text-align: center;'>Niger MLoS</h1>", unsafe_allow_html=True)

# --- Load data from GitHub ---
raw_url = "https://raw.githubusercontent.com/abubakars/mlos-niger-update/refs/heads/main/MLOSS.csv"
resp = requests.get(raw_url)
if resp.status_code == 200:
    df = pd.read_csv(StringIO(resp.text))
else:
    st.error("❌ Failed to load data from GitHub")
    st.stop()

# --- Filter Section ---
st.markdown("### 🔍 Filter by LGA and Ward")
if "lga_name" in df.columns and "ward_name" in df.columns:
    lga_list = sorted(df["lga_name"].dropna().unique())
    ward_list = sorted(df["ward_name"].dropna().unique())

    col1, col2 = st.columns(2)
    with col1:
        selected_lga = st.selectbox("Select LGA", ["All"] + lga_list)
    with col2:
        selected_ward = st.selectbox("Select Ward", ["All"] + ward_list)

    filtered_df = df.copy()
    if selected_lga != "All":
        filtered_df = filtered_df[filtered_df["lga_name"] == selected_lga]
    if selected_ward != "All":
        filtered_df = filtered_df[filtered_df["ward_name"] == selected_ward]
else:
    st.warning("⚠️ Missing columns: 'lga_name' and/or 'ward_name'")
    filtered_df = df.copy()

# --- AG-Grid Config ---
st.markdown("### ✏️ Edit or Add Rows Below")

gb = GridOptionsBuilder.from_dataframe(filtered_df)

# Make all columns editable
gb.configure_default_column(editable=True, resizable=True, wrapText=True, autoHeight=True)

# Allow adding new rows
gb.configure_grid_options(domLayout='autoHeight')

# JS to highlight rows with empty cells
highlight_js = JsCode("""
function(params) {
    let hasEmpty = false;
    for (let key in params.data) {
        if (params.data[key] === null || params.data[key] === '') {
            hasEmpty = true;
            break;
        }
    }
    if (hasEmpty) {
        return { 'backgroundColor': '#fff3cd' };
    }
};
""")

gb.configure_grid_options(getRowStyle=highlight_js)

grid_options = gb.build()

# --- Display editable AG-Grid ---
grid_response = AgGrid(
    filtered_df,
    gridOptions=grid_options,
    enable_enterprise_modules=False,
    update_mode='MODEL_CHANGED',
    data_return_mode='FILTERED_AND_SORTED',
    fit_columns_on_grid_load=True,
    allow_unsafe_jscode=True,
    height=500,
    reload_data=False
)

edited_df = grid_response["data"]

# --- Update full df with changes ---
if not edited_df.equals(filtered_df):
    st.info("🔄 Changes detected and merged into full dataset.")
    df_not_affected = df.copy()
    if selected_lga != "All":
        df_not_affected = df_not_affected[df_not_affected["lga_name"] != selected_lga]
    if selected_ward != "All":
        df_not_affected = df_not_affected[df_not_affected["ward_name"] != selected_ward]
    df = pd.concat([df_not_affected, edited_df], ignore_index=True)

# --- Download full updated table ---
st.download_button(
    label="⬇️ Download Full Updated CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="full_updated_MLOSS.csv",
    mime="text/csv"
)

# --- Expandable full table ---
with st.expander("📋 Show Full Updated Table"):
    st.dataframe(df, use_container_width=True)
