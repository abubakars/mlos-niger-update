import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.markdown("<h1 style='text-align: center;'>Niger MLoS</h1>", unsafe_allow_html=True)

raw_url = "https://raw.githubusercontent.com/abubakars/mlos-niger-update/refs/heads/main/MLOSS.csv"

resp = requests.get(raw_url)
if resp.status_code == 200:
    df = pd.read_csv(StringIO(resp.text))
    st.success("Data loaded successfully from GitHub")
    st.dataframe(df, use_container_width=True)
else:
    st.error("Failed to load CSV from GitHub")
