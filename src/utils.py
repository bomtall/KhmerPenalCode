from datetime import datetime, timedelta
import math
import streamlit as st

def convert_days_to_years(days: float) -> float:
    return round(days/365, 2)

def convert_years_to_days(years: float) -> int:
    return math.ceil(years*365)

def convert_year_to_timedelta(years: float | int) -> timedelta:
    return timedelta(days=convert_years_to_days(years))

def create_sentence_period(years):
    days = convert_years_to_days(years)
    if days < 28:
        return f"{round(days)} days"
    elif 365 > days >= 28:
        return f"{round(days/30)} months"
    elif days >= 365:
        year_value = round(days/365, 1)
        if year_value.is_integer():
            year_value = int(year_value)
        return f"{year_value} years"
    

def add_sidebar_elements():
    st.sidebar.title("Khmer Penal Code Navigator")
    st.sidebar.markdown("Contact: lionelfblackman@gmail.com")
    st.sidebar.markdown("[Penal Code](https://www.ajne.org/sites/default/files/resource/laws/7195/criminal-code-cambodia-en-kh.pdf)")
    st.sidebar.image("./resources/penal_code.png", width=150)
    st.sidebar.markdown("[English Translation](https://www.ajne.org/sites/default/files/resource/laws/7195/criminal-code-cambodia-en-kh.pdf)")
    st.sidebar.image("./resources/eng_translation.png", width=150)
    
    