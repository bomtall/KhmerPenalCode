import json
import streamlit as st

st.set_page_config(
    page_title="Khmer Sentencing Guide",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open("resources/data.json", "r") as f:
    penal_dict = json.load(f)

st.write(penal_dict)