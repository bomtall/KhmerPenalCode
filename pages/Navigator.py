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


with open("resources/data.json", "r") as f:
    penal_dict = json.load(f)

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
        standard_max_sentence = crime_dict["standard"]["prison"]["max"]
        standard_min_sentence = crime_dict["standard"]["prison"]["min"]
        st.metric(label="Maximum prison sentence (years)", value=standard_max_sentence)
        st.metric(label="Minimum prison sentence (years)", value=standard_min_sentence)
with row1[2]:
    st.markdown("#### Standard fines")
    if crime_dropdown:
        standard_max_fine = crime_dict["standard"]["fine"]["max"]
        standard_min_fine = crime_dict["standard"]["fine"]["min"]
        st.metric(label="Maximum fine", value="៛" + millify.millify(standard_max_fine))
        st.metric(label="Minimum fine", value="៛" + millify.millify(standard_min_fine))
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
            captions=["; Or ".join(crime_dict["aggrevations"][x]["clauses"]) for x in crime_dict["aggrevations"]],
            index=None
            )
with row3[0]:
    if crime_dropdown and aggrevations_radio:
        agg_max_sentence = crime_dict["aggrevations"][aggrevations_radio]["prison"]["max"]
        agg_min_sentence = crime_dict["aggrevations"][aggrevations_radio]["prison"]["min"]
        st.metric(label="Aggrevated maximum sentence", value=agg_max_sentence, delta=agg_max_sentence - standard_max_sentence)
        st.metric(label="Aggrevated minimum sentence", value=agg_min_sentence, delta = agg_min_sentence - standard_min_sentence)
with row4[0]:
    st.markdown('---')

st.markdown("## 3. Previous convictions")
st.markdown("Does the indictment cite the previous conviction?")
st.markdown('---')

st.markdown("## 4. Mitigating circumstances")
st.markdown("Are there mitigating circumstances warranted by the nature of the offence or the character of the accused?")
st.markdown('---')

st.markdown("## 5. Initial prison & fine determination")
st.markdown("After sections 2, 3 and 4 what is the minimum and what is the maximum sentence of imprisonment?")
st.markdown('---')

st.markdown("## 6. Suspended sentences")
st.markdown("Is the sentence to be passed at section 5 for the current offence less than 5 years (and a fine)?")
st.markdown('---')

st.markdown("## 7. Additional penalties")
st.markdown("Select any number of additional penalties")
st.markdown('---')

st.markdown("## 8. Final sentence")
st.markdown('---')