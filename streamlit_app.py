import streamlit as st
import pandas as pd
import os

# Title
st.title("Collaborative CSV Editor")

# File uploader
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file:
    # Read CSV
    df = pd.read_csv(uploaded_file)
    original_df = df.copy()

    # Select LGA
   if "lga_name" in df.columns and "ward_name" in df.columns:
    st.markdown("### 🗂️ Filter by LGA and Ward")

    # Column layout for side-by-side filters
    col1, col2 = st.columns(2)

    with col1:
        lga_options = df["lga_name"].dropna().unique().tolist()
        selected_lga = st.selectbox("Select LGA", sorted(lga_options))

    with col2:
        ward_options = df[df["lga_name"] == selected_lga]["ward_name"].dropna().unique().tolist()
        selected_ward = st.selectbox("Select Ward", sorted(ward_options))

    # Apply both filters
    df = df[(df["lga_name"] == selected_lga) & (df["ward_name"] == selected_ward)]
else:
    st.error("Columns `lga_name` and/or `ward_name` not found in CSV.")
    st.stop()


    st.markdown("### 🔍 Filtered & Editable Table")

    # Columns that should NOT be editable
    non_editable_cols = ["lat", "lon", "lga_name", "ward_name"]
    editable_cols = [col for col in df.columns if col not in non_editable_cols]

    # Show editable table
    edited_df = st.data_editor(
        df,
        column_config={col: st.column_config.Column(disabled=True) for col in non_editable_cols if col in df.columns},
        use_container_width=True,
        num_rows="dynamic",
    )

    # Buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Save back to original file"):
            # Write to the same file (overwrite)
            file_path = os.path.join("data", uploaded_file.name)  # you can change this
            edited_df.to_csv(file_path, index=False)
            st.success(f"File saved to {file_path}")

    with col2:
        # Download edited file
        st.download_button(
            label="⬇️ Download Edited CSV",
            data=edited_df.to_csv(index=False).encode("utf-8"),
            file_name=f"edited_{uploaded_file.name}",
            mime="text/csv",
        )
