# import sys
# import toml
import json
import millify
# import requests
# import calendar
# import datetime as dt
import streamlit as st
# from pathlib import Path
from src.sentence_guide import SentenceGuide, Crime, Sentence
import src.utils as utils
from streamlit_float import *
import math


st.set_page_config(
    page_title="Khmer Sentencing Guide",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

bool_dict = {
    "Yes": True,
    "No": False,
    "None": None,
    None: None
}

# utils.add_sidebar_elements()

with open("resources/data.json", "r", encoding="utf-8") as f:
    penal_dict = json.load(f)
    
    
# initialize float feature/capability
# float_init()
    
# row0 = st.columns((1,1))
# row0[0].float("top: 0.15rem;z-index: 999990; background-color: ")
# row0[1].float("top: 0.15rem;z-index: 999990; background-color: ")

# style = '''<style>
# .floating a {
#     color: var(--default-textColor);
#     opacity: 0.4;
#     text-decoration: none;
# }
# .floating a:hover {
#     color: var(--default-textColor)!important;
#     opacity: 1;
# }
# </style>'''
# st.markdown(style, unsafe_allow_html=True)

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
row16 = st.columns((1,1))

crime=None
sentence_guide = SentenceGuide()
if "current_max_s" not in st.session_state:
    st.session_state["current_max_s"] = 0
if "current_min_s" not in st.session_state:
    st.session_state["current_min_s"] = 0

with row1[0]:
    st.markdown("## 1. Offence / បទល្មើស")
    crime_dropdown = st.selectbox("Select crime",  list(penal_dict.keys()), index=None)
    
    if crime_dropdown:
        crime = Crime(penal_dict[crime_dropdown])
        sentence_guide.initialise_with_crime(crime)

with row1[1]:
    st.markdown("#### Standard sentences ប្រយោគស្តង់ដារ")
    if crime_dropdown:
        st.metric(label="Max prison sentence ទោសជាប់ពន្ធនាគារអតិបរមា", value=crime.standard_max_sentence.get_sentence_str())
        st.metric(label="Min prison sentence ទោសដាក់ពន្ធនាគារអប្បបរមា", value=crime.standard_min_sentence.get_sentence_str())

with row1[2]:
    st.markdown("#### Standard fines ការផាកពិន័យស្តង់ដារ")
    if crime and crime.standard_max_fine:
        st.metric(label="Max fine ការផាកពិន័យជាអតិបរមា", value="៛" + millify.millify(crime.standard_max_fine))
        st.metric(label="Minimum fine ការផាកពិន័យអប្បបរមា", value="៛" + millify.millify(crime.standard_min_fine))

with row2[0]:
    st.markdown('---')
    
aggrevations_radio = None
def update_radio():
    st.session_state["current_max_s"] = aggrevations_radio
    
with row3[0]:
    st.markdown("## 2. Aggravating circumstances")
    st.markdown("Only one or none of the three options can apply. If any applicable, then select the most serious")
    aggrevations_radio = st.radio(
        label="Select the most severe article that applies or none",
        options=crime.aggrevation_articles + ["None"] if crime else [None],
        captions=crime.aggrevation_clauses + ["None"] if crime else [None],
        index=None,
        on_change=update_radio
        )
        
if crime and aggrevations_radio:
    sentence_guide.set_agg_max_sentence(aggrevations_radio)
    sentence_guide.set_agg_min_sentence(aggrevations_radio)
   
    #st.session_state.top_bar. = f"### Current max sentence: {sentence_guide.current_max_sentence}. Current min sentence: {sentence_guide.current_min_sentence}", key="top_bar"
    
with row3[1]:
    if sentence_guide.agg_max_sentence:   
        st.metric(
            label="Aggrevated maximum sentence",
            value=sentence_guide.agg_max_sentence.get_sentence_str(),
            delta=None,
            delta_color="inverse"
        )

with row3[2]:
    if sentence_guide.agg_min_sentence:
        st.metric(
            label="Aggrevated minimum sentence",
            value=sentence_guide.agg_min_sentence.get_sentence_str(),
            delta=None,
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
    if sentence_guide.prev_conviction_pardon == False:
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
                   
    if sentence_guide.prev_conviction_pardon == False and sentence_guide.prev_conviction_type in ["Felony", "Misdemeanour"]:
        final_judgement_in_5y = st.selectbox(
                label="Was the previous felony or misdemeanour final judgement within 5 years of the date of the offence?",
                options=["Yes", "No"],
                index=None
            )
        if final_judgement_in_5y == "Yes":
            sentence_guide.final_judgement_in_5y = True

    if sentence_guide.final_judgement_in_5y and sentence_guide.prev_conviction_type == "Felony":
        if sentence_guide.current_max_sentence < 6:
            sentence_guide.set_current_max_sentence(6)

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
            if (sentence_guide.current_max_sentence.unit == "years" and sentence_guide.current_max_sentence.value < 6) or (
                sentence_guide.current_max_sentence.unit != "years"
            ):
                prev_conv_new_sentence = Sentence(6, "years")
                diff = utils.create_sentence_period(prev_conv_new_sentence.value - sentence_guide.current_max_sentence.value)
                sentence_guide.set_current_max_sentence(prev_conv_new_sentence)

                st.metric(
                    label="New maximum sentence",
                    value=sentence_guide.current_max_sentence.get_sentence_str(),
                    delta=diff,
                    delta_color="inverse"
                )
            

with row6[0]:
    st.markdown('---')

with row7[0]:
    st.markdown("## 4. Mitigating circumstances")
    mitigations = st.selectbox(label="Are there mitigating circumstances warranted by the nature of the offence or the character of the accused?", options=["Yes", "No"], index=None)
    if mitigations == "Yes":
        basis_of_mitigations = st.text_area(label="Court to enter basis of finding mitigating circumstances")
        if basis_of_mitigations:
            sentence_guide.basis_of_mitigations = basis_of_mitigations


if mitigations == "Yes":
    with row7[1]:
        min_sentence_diff = sentence_guide.mitigtate_sentence_article_94()
        min_fine_diff = sentence_guide.mitigate_fine_article_94()
        st.metric(
            label="New minimum sentence",
            value=sentence_guide.current_min_sentence.get_sentence_str(),
            delta=min_sentence_diff,
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
    if sentence_guide.current_max_sentence != None:
        if sentence_guide.current_max_sentence.unit == "years" and sentence_guide.current_max_sentence.value <= 3:
            st.markdown("If the maximum at this stage is not more than 3 years imprisonment consider community service or a reprimand (Articles 72 & 76) No fine or imprisonment allowed alongside.")
            community_service = st.selectbox(label="Community Service", options=["Yes", "No"], index=None)
            if community_service == "Yes":
                sentence_guide.community_service = True
                cs_hours = st.slider(label="How many hours of community service?", min_value=30, max_value=200, step=1, value=115)
                cs_timeframe =  st.slider(label="Time for performance of community service in months", max_value=12, step=1, value=6)
                sentence_guide.community_service_hours = cs_hours
                sentence_guide.community_service_timeframe = cs_timeframe
            elif community_service == "No":
                sentence_guide.community_service = False
            

with row9[1]:
    if sentence_guide.community_service == False:
        if sentence_guide.possible_to_reprimand():
            offer_to_reprimand = st.selectbox(label="Offer to suspend Sentence in full or in part (as well as fine)", options=["Yes", "No"], index=None)
            sentence_guide.offer_to_reprimand = bool_dict[offer_to_reprimand]

with row9[2]:
    if crime:
        if sentence_guide.community_service != True:
            st.markdown("If imprisonment or fine what is the sentence the Court intends to pass before consideration of suspending the sentence in whole or part (Stage 6)?")
            if sentence_guide.current_min_sentence.value > 1 and sentence_guide.current_min_sentence.unit == "years":
                years = st.number_input(label="Years", min_value=sentence_guide.current_min_sentence.value, max_value=sentence_guide.current_max_sentence.value)

            else:
                years = st.number_input(label="Years", min_value=0.0, max_value=float(math.ceil(sentence_guide.current_max_sentence.convert_to_years())), step=1.0)
            months = st.number_input(label="Months", min_value=0, max_value=12, step=1)
            weeks = st.number_input(label="Weeks", min_value=0, max_value=4, step=1)
            days = st.number_input(label="Days", min_value=0, max_value=7, step=1)
    
            sum = years+(months/12)+(weeks/52)+(days/365)
            if sum > sentence_guide.current_max_sentence.convert_to_years() or sum < sentence_guide.current_min_sentence.convert_to_years():
                st.markdown(":red[Outside of guideline range]")
            else:
                sentence_input = Sentence(sum, "years")
                st.markdown(f"Sentence: {sentence_input.get_sentence_str()}")
                sentence_guide.intended_sentence = sentence_input
            fine_bool = st.checkbox(label="Intend to fine?")
            if fine_bool:
                fine_input = st.number_input(label="Enter the intended fine amount", min_value=float(sentence_guide.current_min_fine), max_value=float(sentence_guide.current_max_fine))
                fine_slider = st.slider(label="Enter the intended fine amount", min_value=float(sentence_guide.current_min_fine), max_value=float(sentence_guide.current_max_fine), format='៛%d', value=fine_input, disabled=True)
                st.markdown(f"Fine: ៛{millify.millify(fine_input)}")
                sentence_guide.intended_fine = fine_input
            else:
                sentence_guide.intended_fine = 0
                
                
        
with row10[0]:
    st.markdown('---')

with row11[0]:
    st.markdown("## 6. Suspended sentences")
    st.markdown("Is the sentence to be passed at section 5 for the current offence less than 5 years (and a fine)?")
    if sentence_guide.current_min_sentence:
        if sentence_guide.possible_to_reprimand():
            suspend_whole_sentence = st.selectbox(label="Is the prison sentence to be suspended in whole?", options=["Yes", "No"], index=None)
            if suspend_whole_sentence == "No":
                st.markdown("How much to suspend?")
                suspend_unit = st.selectbox(label="Unit", options=["years", "months", "weeks", "days"])
                suspend_amount = st.number_input(label="Amount", step=1)
                sentence_guide.sentence_amount_to_suspend = Sentence(suspend_amount, suspend_unit)
            if suspend_whole_sentence == "Yes":
                sentence_guide.sentence_suspended = True
                
with row11[1]:
    st.markdown("##")
    if sentence_guide.current_min_sentence:
        if sentence_guide.possible_to_reprimand():
            suspend_whole_fine = st.selectbox(label="Is the fine to be suspended in whole?", options=["Yes", "No"], index=None)
            if suspend_whole_fine == "Yes":
                sentence_guide.fine_suspended = True
            elif suspend_whole_fine == "No":
                fine_amount_to_suspend = st.slider(label="Amount to suspend", min_value=0, max_value=sentence_guide.current_max_fine, format='៛%d')
            

with row12[0]:
    st.markdown('---')

with row13[0]:
    st.markdown("## 7. Additional penalties")
    if crime:
        add_penalties = st.multiselect(label="Select any number of additional penalties", options=crime.additional_penalties)
        additional_penalties_list = []
        for penalty in add_penalties:
            st.markdown(f"**{penalty}**")
            u = st.selectbox(label="Unit", options=["years", "months", "weeks", "days"], key="unit"+penalty)
            t = st.number_input(label="Enter given term", step=1, key="amount-" +penalty)
            additional_penalties_list.append([penalty, t, u])
        sentence_guide.additional_penalties = additional_penalties_list
            
        
with row14[0]:
    st.markdown('---')

with row15[0]:
    st.markdown("## 8. Final sentence")
    if sentence_guide.community_service or sentence_guide.intended_sentence or sentence_guide.offer_to_reprimand:
        st.markdown(f"Final sentence: {sentence_guide.intended_sentence.get_sentence_str()} {"SUSPENDED" + " " + sentence_guide.sentence_amount_to_suspend.get_sentence_str() if sentence_guide.sentence_amount_to_suspend else ""} {"SUSPENDED" if sentence_guide.sentence_suspended else ""}")
        st.download_button(label="Download Report", data=f"Final sentence: {sentence_guide.intended_sentence.get_sentence_str()} {"SUSPENDED" if sentence_guide.sentence_suspended else ""}", file_name=None)
        output_str = """
        Final sentence
        """
    
with row16[0]:
    st.markdown('---')
    
with st.sidebar:
    st.text_input(label="Current max sentence", value=st.session_state["current_max_s"], disabled=True)
    st.text_input(label="Current min sentence", value=st.session_state["current_min_s"], disabled=True)
    
    
