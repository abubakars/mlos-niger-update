import streamlit as st
import pandas as pd
import pydeck as pdk

# Set page configuration
st.set_page_config(page_title="CSV Viewer & Map", layout="wide")

# App title
st.title("📍 CSV Viewer with Map Display")

# Upload CSV file
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

# Process file if uploaded
if uploaded_file is not None:
    try:
        # Read CSV into DataFrame
        df = pd.read_csv(uploaded_file)

            # Display full table
            st.subheader("📊 Uploaded Data")
            st.dataframe(df.reset_index(drop=True))

            # Map Display
            st.subheader("🗺️ Map of Locations")
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/streets-v11",
                    initial_view_state=pdk.ViewState(
                        latitude=df["Latitude"].mean(),
                        longitude=df["Longitude"].mean(),
                        zoom=7,
                        pitch=0,
                    ),
                    layers=[
                        pdk.Layer(
                            "ScatterplotLayer",
                            data=df,
                            get_position="[Longitude, Latitude]",
                            get_color="[0, 150, 200, 160]",
                            get_radius=100,
                        )
                    ],
                )
            )

            # Download data
            st.subheader("⬇️ Download Data")
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="full_data.csv",
                mime="text/csv",
            )

    except Exception as e:
        st.error(f"Error reading CSV file: {e}")

else:
    st.info("Please upload a CSV file to begin.")
