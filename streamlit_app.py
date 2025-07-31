import streamlit as st
import pandas as pd
import pydeck as pdk

# Set page config
st.set_page_config(page_title="LGA CSV Filter & Map", layout="wide")

# App title
st.title("📍 CSV Viewer: Filter by LGA & Map Locations")

# Upload CSV file
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

# Process file if uploaded
if uploaded_file is not None:
    # Read CSV into DataFrame
    try:
        df = pd.read_csv(uploaded_file)

        # Check for required columns
        required_columns = {"Name", "LGA", "Latitude", "Longitude"}
        if not required_columns.issubset(df.columns):
            st.error(f"CSV must contain the following columns: {required_columns}")
        else:
            # Drop rows with missing coordinates
            df = df.dropna(subset=["Latitude", "Longitude"])

            # Sidebar filter
            lgas = df["LGA"].unique()
            selected_lga = st.sidebar.selectbox("🏙️ Select LGA to filter", sorted(lgas))

            # Filter data by selected LGA
            filtered_df = df[df["LGA"] == selected_lga]

            # Display filtered table
            st.subheader(f"📊 Filtered Data for {selected_lga}")
            st.dataframe(filtered_df.reset_index(drop=True))

            # Map display
            st.subheader("🗺️ Location Map")
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/streets-v11",
                    initial_view_state=pdk.ViewState(
                        latitude=filtered_df["Latitude"].mean(),
                        longitude=filtered_df["Longitude"].mean(),
                        zoom=10,
                        pitch=0,
                    ),
                    layers=[
                        pdk.Layer(
                            "ScatterplotLayer",
                            data=filtered_df,
                            get_position="[Longitude, Latitude]",
                            get_color="[200, 30, 0, 160]",
                            get_radius=100,
                        )
                    ],
                )
            )

            # Download filtered data
            st.subheader("⬇️ Download Filtered Data")
            csv = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{selected_lga}_filtered_data.csv",
                mime="text/csv",
            )

    except Exception as e:
        st.error(f"Error reading CSV file: {e}")

else:
    st.info("Please upload a CSV file to begin.")
