import streamlit as st
st.markdown(
    "<h1 style='text-align: center; color: #48bbdb;'>Niger MLoS</h1>",
    unsafe_allow_html=True
)
st.markdown("### Upload a CSV file")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File successfully uploaded and read.")
        st.markdown("### Preview of the CSV data:")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error reading the file: {e}")
