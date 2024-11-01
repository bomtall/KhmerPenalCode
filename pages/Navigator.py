import sys
import toml
import json
import scipy
import millify
import gspread
import requests
import calendar
import numpy as np
import pandas as pd
import polars as pl
import datetime as dt
import streamlit as st
from pathlib import Path


penal_dict = {

    "Theft": {
        "standard": {
            "prison": {"min": 6, "max": 36},
            "fine": {"min": 1000000, "max": 6000000}                            
        },
        "aggrevations": {
            "Article 357": {
                "article": "Article 357",
                "clauses": [
                    "Committed by breaking and entering"
                    "Preceded, accompanied or followed by acts of violence"
                    ],
                    "prison": {"min": 36, "max": 120}
            },
            "Article 358": {
                "article": "Article 358",
                "clauses": [
                    "Preceded, accompanied or followed by acts of violence causing mutilation or permanent disability"
                    ],
                    "prison": {"min": 120, "max": 240}
            },
            "Article 359": {
                "article": "Article 359",
                "clauses": [
                    "Preceded, accompanied or followed by torture or acts of cruelty"
                ],
                "prison": {"min": 180, "max": 360}
            }
        }
    }
}


st.set_page_config(
    page_title="Khmer Sentencing Guide",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

row1 = st.columns((1,1,1), gap="medium")
row2 = st.columns(1)
row3 = st.columns((1,1), gap="medium")
row4 = st.columns(1)

with row1[0]:
    st.markdown("## 1. Offence")
    crime_dropdown = st.selectbox("Select crime", ["Theft"], index=None)
if crime_dropdown:
    crime_dict = penal_dict[crime_dropdown]
with row1[1]:
    st.markdown("#### Standard sentences")
    if crime_dropdown:
        st.text_input(label="Maximum prison sentence (months)", value=crime_dict["standard"]["prison"]["max"], disabled=True)
        st.text_input(label="Minimum prison sentence (months)", value=crime_dict["standard"]["prison"]["min"], disabled=True)
with row1[2]:
    st.markdown("#### Standard fines")
    if crime_dropdown:
        st.text_input(label="Maximum fine", value=crime_dict["standard"]["fine"]["max"], disabled=True)
        st.text_input(label="Minimum fine", value=crime_dict["standard"]["fine"]["min"], disabled=True)
with row2[0]:
    st.markdown('---')

with row3[0]:
    st.markdown("## 2. Aggravating circumstances")
    st.markdown("Only one or none of the three options can apply. If any applicable, then select the most serious")
        
with row3[1]:
    if crime_dropdown:
        aggrevations_radio = st.radio(
            label="Select the most severe article that applies or none",
            options=[crime_dict["aggrevations"][x]["article"] for x in crime_dict["aggrevations"]],
            captions=[";".join(crime_dict["aggrevations"][x]["clauses"]) for x in crime_dict["aggrevations"]],
            index=None
            )
with row3[0]:
    if crime_dropdown and aggrevations_radio:
        st.text_input(label="Aggrevated maximum sentence", value=crime_dict["aggrevations"][aggrevations_radio]["prison"]["max"])
        st.text_input(label="Aggrevated minimum sentence", value=crime_dict["aggrevations"][aggrevations_radio]["prison"]["min"])
with row4[0]:
    st.markdown('---')

st.markdown("## 3. Previous convictions")
st.markdown('---')

st.markdown("## 4. Mitigating circumstances")
st.markdown('---')

st.markdown("## 5. Initial prison & fine determination")
st.markdown('---')

st.markdown("## 6. Suspended sentences")
st.markdown('---')

st.markdown("## 7. Additional penalties")
st.markdown('---')

st.markdown("## 8. Final sentence")
st.markdown('---')