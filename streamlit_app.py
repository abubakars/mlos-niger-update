import streamlit as st
import pandas as pd
import os

# App title
st.title("📊 Collaborative CSV Editor")

# Upload CSV
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file:
    # Load CSV into DataFrame
    df = pd.read_csv(uploaded_file)
    original_df = df.copy()

    # Validate required columns
    if "lga_name" not in df.columns or "ward_name" not in df.columns:
        st.error("CSV must contain both 'lga_name' and 'ward_name' columns.")
        st.stop()

    # --- FILTER SECTION ---
    st.markdown("### 🗂️ Filter by LGA and Ward")

    col1, col2 = st.columns(2)

    with col1:
        lga_options = df["lga_name"].dropna().unique().tolist()
        selected_lga = st.selectbox("Select LGA", sorted(lga_options))

    with col2:
        ward_options = df[df["lga_name"] == selected_lga]["ward_name"].dropna().unique().tolist()
        selected_ward = st.selectbox("Select Ward", sorted(ward_options))

    # Apply both filters
    df = df[(df["lga_name"] == selected_lga) & (df["ward_name"] == selected_ward)]

    st.markdown("### ✏️ Editable Table")

    # Columns that should NOT be editable
    non_editable_cols = ["lat", "lon", "lga_name", "ward_name"]
    editable_cols = [col for col in df.columns if col not in non_editable_cols]

    # Setup column configs for read-only fields
    column_config = {
        col: st.column_config.Column(disabled=True) for col in non_editable_cols if col in df.columns
    }

    # Display editable table
    edited_df = st.data_editor(
        df,
        column_config=column_config,
        use_container_width=True,
        num_rows="dynamic",
        key="editable_table"
    )

    # --- ACTIONS: Save or Download ---
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Save to Original File"):
            # Save to disk (optional: change 'data/' path)
            save_path = os.path.join("data", uploaded_file.name)
            os.makedirs("data", exist_ok=True)
            edited_df.to_csv(save_path, index=False)
            st.success(f"Saved to {save_path}")

    with col2:
        st.download_button(
            label="⬇️ Download Edited CSV",
            data=edited_df.to_csv(index=False).encode("utf-8"),
            file_name=f"edited_{uploaded_file.name}",
            mime="text/csv"
        )
