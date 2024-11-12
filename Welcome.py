import sys
import toml
import json
import requests
import calendar
import numpy as np
import datetime as dt
import streamlit as st
from pathlib import Path
from src import utils

# command to run: streamlit run Welcome.py

st.set_page_config(
    page_title="Khmer Sentencing Guide",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

utils.add_sidebar_elements()
    
st.markdown("## Khmer Penal Code Navigator")

st.markdown("The Cambodian (or Khmer) Criminal (or Penal) Code is a 667-article document setting out the ingredients of numerous criminal offences and the range of punishments each crime attracts for the guilty")
st.markdown("This application is designed to aid in the sentencing process and produce guidelines based on the penal code")

