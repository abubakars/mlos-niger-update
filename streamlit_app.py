import streamlit as st
import pandas as pd
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

st.set_page_config(page_title="Local CSV/XLSX Editor", layout="wide")

# CONFIG
FILE_PATH = "data.xlsx"  # change to "data.csv" if using CSV
LOCKED_COLUMNS = ["LGA", "Ward", "Global ID"]
DROPDOWN_OPTIONS = {
    "Status": ["Pending", "Complete", "In Progress"],
    "Category": ["A", "B", "C"]
}

# --- File Utilities
def is_csv():
    return FILE_PATH.lower().endswith(".csv")

@st.cache_data
def load_data():
    if is_csv():
        return pd.read_csv(FILE_PATH)
    else:
        return pd.read_excel(FILE_PATH)

def save_data(df):
    if is_csv():
        df.to_csv(FILE_PATH, index=False)
    else:
        with pd.ExcelWriter(FILE_PATH, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, sheet_name="Sheet1", index=False)

df = load_data()

# --- Sidebar Filters
st.sidebar.header("🔍 Filter")
lga_filter = st.sidebar.selectbox("Select LGA", ["All"] + sorted(df["LGA"].dropna().unique().tolist()))
ward_filter = st.sidebar.selectbox("Select Ward", ["All"] + sorted(df["Ward"].dropna().unique().tolist()))

filtered_df = df.copy()
if lga_filter != "All":
    filtered_df = filtered_df[filtered_df["LGA"] == lga_filter]
if ward_filter != "All":
    filtered_df = filtered_df[filtered_df["Ward"] == ward_filter]

st.title("📄 Local Data Editor")

# --- Editable Grid
with st.expander("📋 View & Edit Table", expanded=True):
    editable_cols = [col for col in filtered_df.columns if col not in LOCKED_COLUMNS]
    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    gb.configure_columns(LOCKED_COLUMNS, editable=False)
    for col in editable_cols:
        if col in DROPDOWN_OPTIONS:
            gb.configure_column(col, editable=True, cellEditor='agSelectCellEditor',
                                cellEditorParams={'values': DROPDOWN_OPTIONS[col]})
        else:
            gb.configure_column(col, editable=True)

    grid_options = gb.build()

    grid_response = AgGrid(
        filtered_df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        fit_columns_on_grid_load=True,
        height=500,
        width='100%',
        reload_data=False,
    )

    updated_df = grid_response["data"]

    if st.button("💾 Save Edits"):
        full_df = df.copy()
        for _, row in updated_df.iterrows():
            match_idx = df[df["Global ID"] == row["Global ID"]].index
            if not match_idx.empty:
                for col in editable_cols:
                    full_df.loc[match_idx, col] = row[col]
        save_data(full_df)
        st.success("File updated successfully!")
        st.rerun()

# --- Add New Row
st.subheader("➕ Add New Entry")

with st.form("add_new_data_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        new_lga = st.text_input("LGA (locked)", disabled=True, value=lga_filter if lga_filter != "All" else "")
        new_ward = st.text_input("Ward (locked)", disabled=True, value=ward_filter if ward_filter != "All" else "")
    with col2:
        next_id = int(df["Global ID"].max()) + 1 if "Global ID" in df.columns and not df["Global ID"].isnull().all() else 1
        new_id = st.text_input("Global ID", value=str(next_id), disabled=True)

    new_data = {}
    for col in df.columns:
        if col in LOCKED_COLUMNS:
            continue
        if col in DROPDOWN_OPTIONS:
            new_data[col] = st.selectbox(f"{col}", DROPDOWN_OPTIONS[col])
        else:
            new_data[col] = st.text_input(f"{col}")

    submitted = st.form_submit_button("🚀 Add Row")
    if submitted:
        new_row = {
            "LGA": new_lga,
            "Ward": new_ward,
            "Global ID": new_id,
            **new_data
        }
        updated_df = df.append(new_row, ignore_index=True)
        save_data(updated_df)
        st.success("Row added successfully!")
        st.rerun()
