import streamlit as st
from src import utils

# command to run: streamlit run Welcome.py

st.set_page_config(
    page_title="Khmer Sentencing Guide",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "### Khmer Penal Code Sentencing Application for Judges  \n This is a demo application created using an open-source and free to use framework called Streamlit  \nContact: lblackman@cltc.law"}
)

utils.add_sidebar_elements()
    
st.markdown("## Khmer Penal Code Sentencing Application for Judges")
st.markdown("""
---
            
This online application is [authorised] for use in [pilot] courts alongside conventional judicial reasoning [for a trial period].

The purpose of the Application is to identify accurately and with efficiency the applicable sentencing powers available to the court when sentencing a convicted offender.

The most serious offence before the Court should be the starting point of the use of the Application. Other lesser offences falling to be sentenced at the same time may be entered after re-setting the Application. The court will subsequently decide whether penalties for two or more offences run concurrently or consecutively.

This is, however, only  a sample Application and is for demonstration purposes only. The offence chosen by the designers for the demonstration is the offence of theft. The option of “murder” is for demonstration only and its presence is to display where the menu of all offences in the Penal Code can be selected in a future fully working Application.

Your feedback is welcome at the end of the operation of the Application. You may use Khmer or English.

---

ឧបករណ៍កាត់ទោសក្រមព្រហ្មទណ្ឌខ្មែរសម្រាប់ចៅក្រម

ឧបករណ៍អនឡាញនេះត្រូវបាន [អនុញ្ញាត] សម្រាប់ប្រើក្នុងតុលាការ [កាត់ក្ដី] ដោយភ្ជាប់ជាមួយហេតុផលតុលាការសាមញ្ញ [សម្រាប់រយៈពេលសាកល្បង]។

គោលបំណងនៃឧបករណ៍នេះគឺដើម្បីកំណត់ឱ្យបានត្រឹមត្រូវ និងមានប្រសិទ្ធភាពនូវអំណាចនៃការកាត់ទោសដែលមានសម្រាប់តុលាការនៅពេលកាត់ទោសជនល្មើសដែលត្រូវបានកាត់ទោស។

បទល្មើសធ្ងន់ធ្ងរបំផុតនៅចំពោះមុខតុលាការគួរតែជាចំណុចចាប់ផ្តើមនៃការប្រើប្រាស់ឧបករណ៍។ បទល្មើសតិចជាងផ្សេងទៀតដែលនឹងត្រូវកាត់ទោសក្នុងពេលតែមួយអាចរួមបញ្ចូលបន្ទាប់ពីកំណត់ឧបករណ៍ឡើងវិញ។ តុលាការ​នឹង​សម្រេច​ជា​បន្តបន្ទាប់​ថា​តើ​ការ​ពិន័យ​សម្រាប់​បទល្មើស​ពីរ​ឬ​ច្រើន​ដំណើរការ​ស្រប​គ្នា​ឬ​ជាប់​គ្នា។

ទោះយ៉ាងណាក៏ដោយ នេះគ្រាន់តែជាឧបករណ៍គំរូមួយប៉ុណ្ណោះ និងសម្រាប់គោលបំណងបង្ហាញតែប៉ុណ្ណោះ។ បទល្មើសដែលត្រូវបានជ្រើសរើសដោយអ្នករចនាសម្រាប់បាតុកម្មគឺការលួច។ ជម្រើសនៃ "ឃាតកម្ម" គឺសម្រាប់គោលបំណងធ្វើបាតុកម្មតែប៉ុណ្ណោះ ហើយមានវត្តមានដើម្បីចង្អុលបង្ហាញកន្លែងដែលម៉ឺនុយនៃបទល្មើសទាំងអស់នៅក្នុងក្រមព្រហ្មទណ្ឌអាចត្រូវបានជ្រើសរើសនៅក្នុងឧបករណ៍ដែលមានមុខងារពេញលេញនាពេលអនាគត។

មតិកែលម្អរបស់អ្នកត្រូវបានស្វាគមន៍នៅចុងបញ្ចប់នៃប្រតិបត្តិការរបស់ឧបករណ៍។ អ្នកអាចប្រើភាសាខ្មែរ ឬភាសាអង់គ្លេស។

---
            
"""
)

st.link_button(
    label="Khmer Penal Code Sentencing Application Feedback. មតិកែលម្អឧបករណ៍ប្រយោគខ្មែរ",
    url="https://docs.google.com/forms/d/e/1FAIpQLSdMB3MTujcwtQRvStg4O1XwrkUN_hu1b1dLLQfTKmA0n8gPbA/viewform"
)
