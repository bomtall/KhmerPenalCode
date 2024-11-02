import sys
import toml
import json
import requests
import calendar
import numpy as np
import datetime as dt
import streamlit as st
from pathlib import Path

# command to run: streamlit run Welcome.py

st.set_page_config(
    page_title="Khmer Sentencing Guide",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.title("Khmer Penal Code Navigator")
    st.markdown("Contact: lionelfblackman@gmail.com")

st.markdown("## Khmer Penal Code Navigator")

st.markdown(
    "The [Cambodian (or Khmer) Criminal (or Penal) Code](http://www.skpcambodia.com/storage/uploads/files/Criminal%20and%20Criminal%20Procedure%20Laws/criminal-code%20Eng.pdf) is a 667-article document setting out the ingredients of numerous criminal offences and the range of punishments each crime attracts for the guilty")