import sys
import toml
import json
import millify
import requests
import calendar
import datetime as dt
import streamlit as st
from pathlib import Path
from src import utils



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
row5 = st.columns((1,1,1), gap="medium")
row6 = st.columns(1)

with row1[0]:
    st.markdown("## 1. Offence")
    crime_dropdown = st.selectbox("Select crime", list(penal_dict.keys()), index=None)
    if crime_dropdown:
        crime_dict = penal_dict[crime_dropdown]
        crime = utils.SentenceGuide(crime_dict)
with row1[1]:
    st.markdown("#### Standard sentences")
    if crime_dropdown:
        st.metric(label="Maximum prison sentence (years)", value=crime.standard_max_sentence)
        st.metric(label="Minimum prison sentence (years)", value=crime.standard_min_sentence)
with row1[2]:
    
    if crime_dropdown and crime.standard_max_fine:
        st.markdown("#### Standard fines")
        st.metric(label="Maximum fine", value="៛" + millify.millify(crime.standard_max_fine))
        st.metric(label="Minimum fine", value="៛" + millify.millify(crime.standard_min_fine))
with row2[0]:
    st.markdown('---')

with row3[0]:
    st.markdown("## 2. Aggravating circumstances")
    st.markdown("Only one or none of the three options can apply. If any applicable, then select the most serious")
        
with row3[1]:
    if crime_dropdown:
        aggrevations_radio = st.radio(
            label="Select the most severe article that applies or none",
            options=crime.aggrevation_articles + ["None"],
            captions=crime.aggrevation_clauses + ["None"],
            index=None
            )
with row3[0]:
    if crime_dropdown and aggrevations_radio and aggrevations_radio != "None":
        crime.set_agg_max_sentence(aggrevations_radio)
        crime.set_agg_min_sentence(aggrevations_radio)
        st.metric(
            label="Aggrevated maximum sentence",
            value=crime.agg_max_sentence,
            delta=crime.agg_max_sentence - crime.standard_max_sentence,
            delta_color="inverse"
        )
        st.metric(
            label="Aggrevated minimum sentence",
            value=crime.agg_min_sentence,
            delta=crime.agg_min_sentence - crime.standard_min_sentence,
            delta_color="inverse"
        )
with row4[0]:
    st.markdown('---')

with row5[0]:
    st.markdown("## 3. Previous convictions")
if crime_dropdown and aggrevations_radio:
    with row5[0]:    
        prev_conviction = st.selectbox(label="Does the indictment cite the previous conviction?", options=["Yes", "No"], index=None)
        if prev_conviction == "Yes":
            crime.prev_conviction = True
        elif prev_conviction == "No":
            crime.prev_conviction = False
        
        if crime.prev_conviction:
            prev_conviction_pardon = st.selectbox(label="Has the previous conviction been pardoned?", options=["Yes", "No"], index=None)
            if prev_conviction_pardon == "Yes":
                crime.prev_conviction_pardon = True
            elif prev_conviction_pardon == "No":
                crime.prev_conviction_pardon = False
    with row5[1]:
        if crime.prev_conviction and crime.prev_conviction_pardon == False:
            st.selectbox(
                label="Was the previous conviction a felony, misdemeanour or petty offence?",
                options=["Felony", "Misdemeanour", "Petty offence"],
                index=None                             
            )
    with row5[2]:
        if prev_conviction == "Yes" and prev_conviction_pardon == "No":
            st.markdown(
    """
    Felony: 5 years to life imprisonment  \n
    Misdemeanour: 7 days to 5 years imprisonment  \n
    Petty Offence: fine or up to 6 days in prison
    """ 
            )

with row6[0]:
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