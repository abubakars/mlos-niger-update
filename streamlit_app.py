import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Editable Table with Map", layout="wide")

st.title("📊 Editable Table + 🗺️ Map Viewer")

# Upload Excel file
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("1️⃣ Preview of Uploaded Data")
    st.dataframe(df.head())

    if "Latitude" in df.columns and "Longitude" in df.columns:
        st.subheader("2️⃣ Edit Table (some columns locked)")

        # Create editable AgGrid
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_column("Name", editable=False)
        gb.configure_column("Latitude", editable=False)
        gb.configure_column("Longitude", editable=False)
        grid_options = gb.build()

        grid_response = AgGrid(df, gridOptions=grid_options, editable=True)
        updated_df = grid_response['data']

        st.subheader("3️⃣ Map of Coordinates")

        m = folium.Map(location=[updated_df["Latitude"].mean(), updated_df["Longitude"].mean()], zoom_start=6)

        for _, row in updated_df.iterrows():
            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=f"{row['Name']}",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

        st_data = st_folium(m, width=900, height=500)

        # Option to download updated data
        st.subheader("💾 Download Updated Data")
        updated_csv = updated_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download as CSV", data=updated_csv, file_name="updated_data.csv", mime="text/csv")

    else:
        st.error("Uploaded file must contain 'Latitude' and 'Longitude' columns.")
else:
    st.info("👆 Please upload an Excel file with columns: Name, Latitude, Longitude, etc.")
