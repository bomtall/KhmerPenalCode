import json
import streamlit as st
from src import utils

st.set_page_config(
    page_title="Khmer Sentencing Guide",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open("resources/data.json", "r") as f:
    penal_dict = json.load(f)

utils.add_sidebar_elements()

st.write(penal_dict)