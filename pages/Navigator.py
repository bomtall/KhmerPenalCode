# import sys
# import toml
import json
import millify
# import requests
# import calendar
# import datetime as dt
import streamlit as st
# from pathlib import Path
from src.sentence_guide import SentenceGuide, Crime


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

crime=None

with row1[0]:
    st.markdown("## 1. Offence")
    crime_dropdown = st.selectbox("Select crime", list(penal_dict.keys()), index=None)
    
    if crime_dropdown:
        crime = Crime(penal_dict[crime_dropdown])
        sentence_guide = SentenceGuide(crime)
        
with row1[1]:
    st.markdown("#### Standard sentences")
    if crime_dropdown:
        st.metric(label="Maximum prison sentence (years)", value=crime.standard_max_sentence)
        st.metric(label="Minimum prison sentence (years)", value=crime.standard_min_sentence)

with row1[2]:
    if crime and crime.standard_max_fine:
        st.markdown("#### Standard fines")
        st.metric(label="Maximum fine", value="៛" + millify.millify(crime.standard_max_fine))
        st.metric(label="Minimum fine", value="៛" + millify.millify(crime.standard_min_fine))

with row2[0]:
    st.markdown('---')

with row3[0]:
    st.markdown("## 2. Aggravating circumstances")
    st.markdown("Only one or none of the three options can apply. If any applicable, then select the most serious")
        
with row3[1]:
    if crime:
        aggrevations_radio = st.radio(
            label="Select the most severe article that applies or none",
            options=crime.aggrevation_articles + ["None"],
            captions=crime.aggrevation_clauses + ["None"],
            index=None
            )
with row3[0]:
    if crime and aggrevations_radio and aggrevations_radio != "None":
        sentence_guide.set_agg_max_sentence(aggrevations_radio)
        sentence_guide.set_agg_min_sentence(aggrevations_radio)
        st.metric(
            label="Aggrevated maximum sentence",
            value=sentence_guide.agg_max_sentence,
            delta=sentence_guide.agg_max_sentence - crime.standard_max_sentence,
            delta_color="inverse"
        )
        st.metric(
            label="Aggrevated minimum sentence",
            value=sentence_guide.agg_min_sentence,
            delta=sentence_guide.agg_min_sentence - crime.standard_min_sentence,
            delta_color="inverse"
        )
with row4[0]:
    st.markdown('---')

with row5[0]:
    st.markdown("## 3. Previous convictions")
if crime and aggrevations_radio:
    with row5[0]:    
        prev_conviction = st.selectbox(label="Does the indictment cite the previous conviction?", options=["Yes", "No"], index=None)
        if prev_conviction == "Yes":
            sentence_guide.prev_conviction = True
        elif prev_conviction == "No":
            sentence_guide.prev_conviction = False
        
        if sentence_guide.prev_conviction:
            prev_conviction_pardon = st.selectbox(label="Has the previous conviction been pardoned?", options=["Yes", "No"], index=None)
            if prev_conviction_pardon == "Yes":
                sentence_guide.prev_conviction_pardon = True
            elif prev_conviction_pardon == "No":
                sentence_guide.prev_conviction_pardon = False
    with row5[1]:
        if sentence_guide.prev_conviction and sentence_guide.prev_conviction_pardon == False:
            st.markdown(
                """
                **Definitions**  \n
                **Felony**: *From five years to life imprisonment*  \n
                **Misdemeanour**: *from seven days up to five years imprisonment*  \n
                **Petty Offence**: *A fine or up to 6 days in prison*
                """
            )
            prev_conviction_type = st.selectbox(
                label="Was the previous conviction a felony, misdemeanour or petty offence?  \n If both felony & misdemeanour apply, select felony",
                options=["Felony", "Misdemeanour", "Petty offence"],
                index=None                             
            )
            sentence_guide.prev_conviction_type = prev_conviction_type
    with row5[2]:       
        if sentence_guide.prev_conviction_type in ["Felony", "Misdemeanour"]:
            felony_misd_pronounced_5y = st.selectbox(
                label="Was a suspended sentence for any misdemeanour or felony pronounced within 5 years before the offence? (Art 109)",
                options=["Yes", "No"],
                index=None
            )
            if felony_misd_pronounced_5y:
                sentence_guide.felony_misd_pronounced_5y = bool(felony_misd_pronounced_5y)
            if sentence_guide.felony_misd_pronounced_5y:
                st.markdown(
                    "**Note:** the prior suspended sentence is revoked and the applicable penalty for the new offence will not run concurrently"
                )
                special_reasons = st.selectbox(
                    label="Are there any special reasons not to revoke a prior suspended sentence? (Art 110)",
                    options=["Yes", "No"],
                    index=None
                )
                if special_reasons == "Yes":
                    sentence_guide.special_revoke_reasons = st.text_input(label="Please give reasons")
                    
        if sentence_guide.prev_conviction and not sentence_guide.prev_conviction_pardon and sentence_guide.prev_conviction_type in ["Felony", "Misdemeanour"]:
             final_judgement_in_5y = st.selectbox(
                    label="Was the previous felony or misdemeanour final judgement within 5 years of the date of the offence?",
                    options=["Yes", "No"],
                    index=None
                )
             if final_judgement_in_5y:
                sentence_guide.final_judgement_in_5y = True
        if sentence_guide.final_judgement_in_5y and sentence_guide.prev_conviction_type == "Felony":
            if sentence_guide.current_max_sentence < 6:
                sentence_guide.current_max_sentence = 6
                st.metric(
                    label="New maximum sentence",
                    value=sentence_guide.current_max_sentence,
                    delta=sentence_guide.current_max_sentence - crime.standard_max_sentence,
                    delta_color="inverse"
                )
            
        if sentence_guide.final_judgement_in_5y and sentence_guide.prev_conviction_type == "Misdemeanour":
            prev_conviction_theft_trust_fraud = st.selectbox(
                label="Was the previous conviction for: Theft, breach of trust or fraud?",
                options=["Yes", "No"],
                index=None
            )
            if prev_conviction_theft_trust_fraud == "Yes":
                sentence_guide.prev_conviction_theft_trust_fraud = True
                if sentence_guide.current_max_sentence < 6:
                    sentence_guide.current_max_sentence = 6
                    st.metric(
                        label="New maximum sentence",
                        value=sentence_guide.current_max_sentence,
                        delta=sentence_guide.current_max_sentence - crime.standard_max_sentence,
                        delta_color="inverse"
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