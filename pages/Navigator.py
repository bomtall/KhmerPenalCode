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
import src.utils as utils


st.set_page_config(
    page_title="Khmer Sentencing Guide",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

utils.add_sidebar_elements()

with open("resources/data.json", "r") as f:
    penal_dict = json.load(f)


row1 = st.columns((1,1,1), gap="medium")
row2 = st.columns(1)
row3 = st.columns((2,1,1), gap="medium")
row4 = st.columns(1)
row5 = st.columns((1,1,1), gap="medium")
row6 = st.columns(1)
row7 = st.columns((2,1,1), gap="medium")
row8 = st.columns(1)
row9 = st.columns((1,1,1), gap="medium")
row10 = st.columns(1)
row11 = st.columns((1,1,1), gap="medium")
row12 = st.columns(1)
row13 = st.columns((1), gap="medium")
row14 = st.columns(1)
row15 = st.columns((1,1,1), gap="medium")
row16 = st.columns(1)

crime=None
sentence_guide = SentenceGuide()

with row1[0]:
    st.markdown("## 1. Offence")
    crime_dropdown = st.selectbox("Select crime", list(penal_dict.keys()), index=None)
    
    if crime_dropdown:
        crime = Crime(penal_dict[crime_dropdown])
        sentence_guide.initialise_with_crime(crime)
        
with row1[1]:
    st.markdown("#### Standard sentences")
    if crime_dropdown:
        st.metric(label="Maximum prison sentence", value=utils.create_sentence_period(crime.standard_max_sentence))
        st.metric(label="Minimum prison sentence", value=utils.create_sentence_period(crime.standard_min_sentence))

with row1[2]:
    st.markdown("#### Standard fines")
    if crime and crime.standard_max_fine:
        st.metric(label="Maximum fine", value="៛" + millify.millify(crime.standard_max_fine))
        st.metric(label="Minimum fine", value="៛" + millify.millify(crime.standard_min_fine))

with row2[0]:
    st.markdown('---')


with row3[0]:
    st.markdown("## 2. Aggravating circumstances")
    st.markdown("Only one or none of the three options can apply. If any applicable, then select the most serious")
    if crime:
        aggrevations_radio = st.radio(
            label="Select the most severe article that applies or none",
            options=crime.aggrevation_articles + ["None"],
            captions=crime.aggrevation_clauses + ["None"],
            index=None
            )
        if aggrevations_radio:
            sentence_guide.set_agg_max_sentence(aggrevations_radio)
            sentence_guide.set_agg_min_sentence(aggrevations_radio)
    
with row3[1]:
    if sentence_guide.agg_max_sentence:   
        st.metric(
            label="Aggrevated maximum sentence",
            value=utils.create_sentence_period(sentence_guide.agg_max_sentence),
            delta=sentence_guide.agg_max_sentence - crime.standard_max_sentence,
            delta_color="inverse"
        )

with row3[2]:
    if sentence_guide.agg_min_sentence:
        st.metric(
            label="Aggrevated minimum sentence",
            value=utils.create_sentence_period(sentence_guide.agg_min_sentence),
            delta=sentence_guide.agg_min_sentence - crime.standard_min_sentence,
            delta_color="inverse"
        )
        
with row4[0]:
    st.markdown('---')
    

with row5[0]:
    st.markdown("## 3. Previous convictions")
    
    if crime and aggrevations_radio:
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
        if sentence_guide.prev_conviction and sentence_guide.prev_conviction_pardon == False:
            st.markdown(
                """
                **Definitions**  \n
                **Felony**: *From five years to life imprisonment*  \n
                **Misdemeanour**: *from seven days up to five years imprisonment*  \n
                **Petty Offence**: *A fine or up to 6 days in prison*
                """
            )

with row5[1]:
    if crime and aggrevations_radio and sentence_guide.prev_conviction_pardon == False:
        prev_conviction_type = st.selectbox(
            label="Was the previous conviction a felony, misdemeanour or petty offence?  \n If both felony & misdemeanour apply, select felony",
            options=["Felony", "Misdemeanour", "Petty offence"],
            index=None                             
        )
        sentence_guide.prev_conviction_type = prev_conviction_type
        
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
                    
with row5[2]:                   
    if crime and aggrevations_radio:                   
        if sentence_guide.prev_conviction_pardon == False and sentence_guide.prev_conviction_type in ["Felony", "Misdemeanour"]:
            final_judgement_in_5y = st.selectbox(
                    label="Was the previous felony or misdemeanour final judgement within 5 years of the date of the offence?",
                    options=["Yes", "No"],
                    index=None
                )
            sentence_guide.final_judgement_in_5y = True if final_judgement_in_5y == "Yes" else False

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
                        value=utils.create_sentence_period(sentence_guide.current_max_sentence),
                        delta=sentence_guide.current_max_sentence - crime.standard_max_sentence,
                        delta_color="inverse"
                    )
            

with row6[0]:
    st.markdown('---')

with row7[0]:
    st.markdown("## 4. Mitigating circumstances")
    mitigations = st.selectbox(label="Are there mitigating circumstances warranted by the nature of the offence or the character of the accused?", options=["Yes", "No"], index=None)
    if mitigations == "Yes":
        basis_of_mitigations = st.text_area(label="Court to enter basis of finding mitigating circumstances")

if mitigations == "Yes":
    with row7[1]:
            min_fine_diff = sentence_guide.mitigate_fine_article_94()
            min_sentence_diff = sentence_guide.mitigtate_sentence_article_94()
            st.metric(
                label="New minimum sentence",
                value=utils.create_sentence_period(sentence_guide.current_min_sentence),
                delta=utils.create_sentence_period(min_sentence_diff),
                delta_color="inverse"
            )
    with row7[2]:
            st.metric(
                label="New minimum fine",
                value="៛" + millify.millify(sentence_guide.current_min_fine),
                delta=millify.millify(min_fine_diff),
                delta_color="inverse"
            )

with row8[0]:
    st.markdown('---')

with row9[0]:
    st.markdown("## 5. Initial prison & fine determination")
    st.markdown("After sections 2, 3 and 4 what is the minimum and what is the maximum sentence of imprisonment?")
    
with row10[0]:
    st.markdown('---')

with row11[0]:
    st.markdown("## 6. Suspended sentences")
    st.markdown("Is the sentence to be passed at section 5 for the current offence less than 5 years (and a fine)?")

with row12[0]:
    st.markdown('---')

with row13[0]:
    st.markdown("## 7. Additional penalties")
    if crime:
        add_penalties = st.multiselect(label="Select any number of additional penalties", options=crime.additional_penalties)
        for penalty in add_penalties:
            st.number_input(label=f"{penalty}: Enter given term")


with row14[0]:
    st.markdown('---')

with row15[0]:
    st.markdown("## 8. Final sentence")
    
with row16[0]:
    st.markdown('---')