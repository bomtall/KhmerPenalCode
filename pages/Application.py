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
    

row0 = st.columns((1))
row1 = st.columns((1,1,1), gap="medium")
row2 = st.columns(1)
row3 = st.columns((1), gap="medium")
row4 = st.columns(1)
row5 = st.columns((1,1,1), gap="medium")
row6 = st.columns(1)
row7 = st.columns((2,1,1), gap="medium")
row8 = st.columns(1)
row9 = st.columns((1,1,1), gap="medium")
row10 = st.columns(1)
row11 = st.columns((1,1,1), gap="medium")
row11point5 = st.columns((2,1))
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

with row0[0]:
    st.markdown("## 1. Offence / បទល្មើស")
with row1[0]:
    crime_dropdown = st.selectbox("Select crime / ជ្រើសរើសបទឧក្រិដ្ឋ",  list(penal_dict.keys()), index=None)
    
    if crime_dropdown:
        crime = Crime(penal_dict[crime_dropdown])
        sentence_guide.initialise_with_crime(crime)
        
with row1[1]:
    st.markdown("#### Standard sentences ប្រយោគស្តង់ដារ")
    if crime_dropdown:
        st.metric(label="Max prison sentence ទោសជាប់ពន្ធនាគារអតិបរមា", value=crime.standard_max_sentence.get_sentence_str())
        st.metric(label="Min prison sentence ទោសដាក់ពន្ធនាគារអប្បបរមា", value=crime.standard_min_sentence.get_sentence_str())
        st.session_state["current_max_s"] = crime.standard_max_sentence.get_sentence_str()
        st.session_state["current_min_s"] = crime.standard_min_sentence.get_sentence_str()
    
    
with row1[2]:
    st.markdown("#### Standard fines ការផាកពិន័យស្តង់ដារ")
    if crime and crime.standard_max_fine:
        st.metric(label="Max fine ការផាកពិន័យជាអតិបរមា", value="៛" + millify.millify(crime.standard_max_fine))
        st.metric(label="Minimum fine ការផាកពិន័យអប្បបរមា", value="៛" + millify.millify(crime.standard_min_fine))

with row2[0]:
    st.markdown('---')
    st.markdown("## 2. Aggravating circumstances / ស្ថានការណ៍កាន់តែធ្ងន់ធ្ងរ")
    
aggrevations_radio = None
def update_radio():
    st.session_state["current_max_s"] = aggrevations_radio
    
with row3[0]:
    st.markdown(
        "Only one or none of the aggravating circumstances need to be applied. If more than one aggravating circumstance applies, select the most serious. The options are ranked in order of height of seriousness.  \n / មានតែកាលៈទេសៈមួយ ឬគ្មានស្ថានទម្ងន់ទោសប៉ុណ្ណោះដែលត្រូវអនុវត្ត។ ប្រសិនបើ​មាន​ស្ថាន​ទម្ងន់​ទោស​ច្រើន​ជាង​មួយ សូម​ជ្រើសរើស​ករណី​ធ្ងន់ធ្ងរ​បំផុត។")
    aggrevations_radio = st.radio(
        label="",
        options=crime.aggrevation_articles[::-1]+["None"]  if crime else [None],
        captions=crime.aggrevation_clauses[::-1]+["None"] if crime else [None],
        index=None,
        on_change=update_radio
        )
        
if crime and aggrevations_radio:
    sentence_guide.set_agg_max_sentence(aggrevations_radio)
    sentence_guide.set_agg_min_sentence(aggrevations_radio)
    if aggrevations_radio != "None":
        sentence_guide.aggrevation = aggrevations_radio

        
with row4[0]:
    st.markdown('---')
    st.markdown("## 3. Previous convictions / ការផ្តន្ទាទោសពីមុន")

with row5[0]:
    
    
    if crime and aggrevations_radio:
        prev_conviction = st.selectbox(label="Does the offender have any previous convictions? / តើ​ជន​ល្មើស​មាន​ការ​ផ្ដន្ទាទោស​មុន​ទេ?", options=["Yes", "No"], index=None)
        if prev_conviction == "Yes":
            cite_prev_conviction = st.selectbox(label="Does the indictment cite the previous conviction? / តើ​ដីកា​ចោទ​ប្រកាន់​លើក​មុន​ឬ​ទេ?", options=["Yes", "No"], index=None)
            if prev_conviction == "Yes" and cite_prev_conviction == "Yes":
                sentence_guide.prev_conviction = True
            elif cite_prev_conviction == "No":
                sentence_guide.prev_conviction = False
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
            sentence_guide.felony_misd_pronounced_5y = bool_dict[felony_misd_pronounced_5y]
            
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
                   
    if sentence_guide.prev_conviction_pardon == False and sentence_guide.prev_conviction_type in ["Felony", "Misdemeanour"] and felony_misd_pronounced_5y == "No":
        final_judgement_in_5y = st.selectbox(
                label="Was the previous felony or misdemeanour final judgement within 5 years of the date of the offence?",
                options=["Yes", "No"],
                index=None
            )
        if final_judgement_in_5y == "Yes":
            sentence_guide.final_judgement_in_5y = True

    if sentence_guide.final_judgement_in_5y and sentence_guide.prev_conviction_type == "Felony":
        if sentence_guide.current_max_sentence.value < 6:
            sentence_guide.set_current_max_sentence(Sentence(6, "years"))

            st.metric(
                label="New maximum sentence",
                value=sentence_guide.current_max_sentence.get_sentence_str(),
                delta=sentence_guide.current_max_sentence.value - crime.standard_max_sentence.value,
                delta_color="inverse"
            )
        
    if sentence_guide.final_judgement_in_5y and sentence_guide.prev_conviction_type == "Misdemeanour":
        prev_conviction_theft_trust_fraud = st.selectbox(
            label="Was the previous conviction for: Theft, breach of trust or fraud? / តើការកាត់ទោសពីមុនសម្រាប់៖ លួច រំលោភលើទំនុកចិត្ត ឬការក្លែងបន្លំ?",
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
    st.markdown("## 4. Mitigating circumstances / កាលៈទេសៈបន្ធូរបន្ថយ")
    
with row7[0]:
    mitigations = st.selectbox(
        label="Are there mitigating circumstances warranted by the nature of the offence or the character of the accused? / តើមានកាលៈទេសៈបន្ធូរបន្ថយដែលធានាដោយលក្ខណៈនៃបទល្មើស ឬចរិតលក្ខណៈរបស់ជនជាប់ចោទ?",
        options=["Yes", "No"], index=None)
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
    st.markdown("## 5. Initial prison & fine determination / ពន្ធនាគារដំបូង និងការកំណត់ការផាកពិន័យ")

with row9[0]:
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
    if crime:
        if sentence_guide.community_service != True and sentence_guide.current_min_sentence:
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
                st.markdown(f"Sentence: {int(years)} years, {months} months, {weeks} weeks, {days} days")
                sentence_guide.intended_sentence = sentence_input
                sentence_guide.intended_sentence_str = f"{int(years)} years, {months} months, {weeks} weeks, {days} days"

                
with row9[2]:
    
    fine_bool = st.checkbox(label="Intend to fine?")
    if fine_bool:
        fine_input = st.number_input(label="Enter the intended fine amount", min_value=float(sentence_guide.current_min_fine), max_value=float(sentence_guide.current_max_fine), step=10000.00)
        fine_slider = st.slider(label="Enter the intended fine amount", min_value=float(sentence_guide.current_min_fine), max_value=float(sentence_guide.current_max_fine), format='៛%d', value=fine_input, disabled=True)
        st.markdown(f"Fine: ៛{millify.millify(fine_input)}")
        sentence_guide.intended_fine = fine_input
    else:
        sentence_guide.intended_fine = 0
                
                
        
with row10[0]:
    st.markdown('---')
    st.markdown("## 6. Suspended sentences / ប្រយោគដែលផ្អាក")

with row11[0]:
    st.markdown("Is the sentence to be passed at section 5 for the current offence less than 5 years (and a fine)?")
    if sentence_guide.intended_sentence:
        if sentence_guide.possible_to_reprimand() and sentence_guide.intended_sentence:
            if not sentence_guide.community_service and sentence_guide.intended_sentence.value <  5:
                offer_to_reprimand = st.selectbox(label="Offer to suspend Sentence in full or in part (as well as fine)", options=["Yes", "No"], index=None)
                sentence_guide.offer_to_reprimand = bool_dict[offer_to_reprimand]
            
with row11[1]:
    st.markdown("##")
    if sentence_guide.offer_to_reprimand:
        suspend_whole_sentence = st.selectbox(label="Is the prison sentence to be suspended in whole?", options=["Yes", "No"], index=None)
        if suspend_whole_sentence == "No":
            st.markdown("How much to suspend?")
            suspend_unit = st.selectbox(label="Unit", options=["years", "months", "weeks", "days"])
            suspend_amount = st.number_input(label="Amount", step=1)
            sentence_guide.sentence_amount_to_suspend = Sentence(suspend_amount, suspend_unit)
        if suspend_whole_sentence == "Yes":
            sentence_guide.sentence_suspended = True
                
with row11[2]:
    st.markdown("##")
    if sentence_guide.offer_to_reprimand and fine_bool:
        if sentence_guide.possible_to_reprimand():
            suspend_whole_fine = st.selectbox(label="Is the fine to be suspended in whole?", options=["Yes", "No"], index=None)
            if suspend_whole_fine == "Yes":
                sentence_guide.fine_suspended = True
            elif suspend_whole_fine == "No":
                fine_amount_to_suspend = st.slider(label="Amount to suspend", min_value=0.0, max_value=float(sentence_guide.intended_fine), format='៛%d')
                sentence_guide.fine_amount_to_suspend = fine_amount_to_suspend
                
with row11point5[0]:
    if sentence_guide.sentence_amount_to_suspend:
        if ((sentence_guide.sentence_suspended or sentence_guide.sentence_amount_to_suspend) and 
        (sentence_guide.intended_sentence.convert_to_years() < 5 and sentence_guide.intended_sentence.convert_to_years() > 0.5)
        ):
            probation_length = st.slider(label="If probation is to be ordered state length of probation between one and three years (in months)", min_value=0, max_value=36)
            probation_measures = st.multiselect(
                label="Select Probation Measures",
                options=[
                    "(1) to remain in employment",
                    "(2) to follow a course of instruction or vocational training",
                    "(3) to take up residence in a specified place",
                    "(4) to undergo medical examination or treatment",  
                    "(5) to demonstrate that he or she is contributing to his or her family's expenses",
                    "(6) to repair, pursuant to his or her means, the harm caused by the offence",
                    "(7) to demonstrate that he or she is paying, pursuant to his or her means, the amounts  owing to the State as a result of his or her conviction",
                    "(8) not to engage in the professional or social activity as specified by the court which  enabled or facilitated the commission of the offence",
                    "(9) not to be present in such places as specified by the court",
                    "(10) not to frequent gambling places",
                    "(11) not to frequent drinking establishments",
                    "(12) not to associate with certain persons as specified by the court, especially the  perpetrator, co-perpetrators, instigators, accomplices or victims of the offence",
                    "(13) not to have or carry any weapon, explosive or ammunition of any kind"
                ]
            )
            if probation_length > 0:
                sentence_guide.probation_length_months = probation_length
                if probation_measures:
                    sentence_guide.probation_measures = probation_measures
            

with row12[0]:
    st.markdown('---')
    st.markdown("## 7. Additional penalties / ការពិន័យបន្ថែម")

with row13[0]:
    
    if crime:
        add_penalties = st.multiselect(label="Select any number of additional penalties", options=crime.additional_penalties)
        additional_penalties_list = []
        for penalty in add_penalties:
            st.markdown(f"**{penalty}**")
            u = st.selectbox(label="Unit", options=["years", "months", "weeks", "days"], key="unit"+penalty)
            t = st.number_input(label="Enter given term", step=1, key="amount-" + penalty)
            additional_penalties_list.append([penalty, t, u])
        sentence_guide.additional_penalties = additional_penalties_list    
        
with row14[0]:
    st.markdown('---')
    st.markdown("## 8. Final sentence / ប្រយោគចុងក្រោយ")

with row15[0]:
    
    if sentence_guide.intended_sentence or sentence_guide.community_service:
        data = sentence_guide.generate_report()
        st.markdown(data)
        st.download_button(label="Download Report", data=data, file_name="Sentence Guidelines Report.txt")

with row16[0]:
    st.markdown('---')
    
with st.sidebar:
    st.markdown("## Khmer Penal Code Sentencing Application")
    
    if crime and sentence_guide.current_max_sentence:
        st.markdown("### Sentencing range")
        st.markdown(f"Current max sentence: **{sentence_guide.current_max_sentence.get_sentence_str()}**")
        st.markdown(f"Current min sentence: **{sentence_guide.current_min_sentence.get_sentence_str()}**")
        st.markdown(f"Current max fine: **៛{millify.millify(sentence_guide.current_max_fine)}**")
        st.markdown(f"Current min fine: **៛{millify.millify(sentence_guide.current_min_fine)}**")
    
st.link_button(
    label="Khmer Penal Code Sentencing Application Feedback. មតិកែលម្អឧបករណ៍ប្រយោគខ្មែរ",
    url="https://docs.google.com/forms/d/e/1FAIpQLSdMB3MTujcwtQRvStg4O1XwrkUN_hu1b1dLLQfTKmA0n8gPbA/viewform"
)
    

    
    
