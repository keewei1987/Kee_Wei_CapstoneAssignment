__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st

from utility import check_password

import os
import openai
from dotenv import load_dotenv

# Add the helpfunctions directory to the Python path
sys.path.append(os.path.abspath("helpfunctions"))

from helperfunctions.crewai import crew
#from crewai import kickoff

# region <--------- Streamlit Page Configuration --------->

st.set_page_config(
    layout="centered",
    page_title="My Capstone Project"
)

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

# endregion <--------- Streamlit Page Configuration --------->

expander = st.expander("IMPORTANT NOTICE")
expander.write('''
    IMPORTANT NOTICE: This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.
Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.
Always consult with qualified professionals for accurate and personalized advice.
''')

         
st.title("Streamlit App - Capstone Assignment")
form = st.form(key="form")
form.subheader("Prompt")

# Initialize session state for user prompt
if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""

# Text area widget with session state to manage its value
user_prompt = form.text_area("Enter your prompt here", value=st.session_state.user_prompt, height=200)

# Define functions to update session state without rerun
def set_preset():
    st.session_state.user_prompt = "How to apply for Employment Pass"

def clear_entry():
    st.session_state.user_prompt = ""

# Add buttons for setting preset and clearing entry
preset_button = form.form_submit_button("Suggested Prompt 1", on_click=set_preset)
clear_button = form.form_submit_button("Clear Entry", on_click=clear_entry)
#submit_button = form.form_submit_button("Submit")

#if form.form_submit_button("Submit", key="submit_button"):
if form.form_submit_button("Submit"):

    st.toast(f"User Input Submitted - {user_prompt}")

     # Call crew.kickoff function and display result
    try:
        results = crew.kickoff(inputs={"topic": user_prompt})  # Trigger kickoff only when Submit is clicked
        st.markdown(results)
    except AttributeError:
        st.error("Error: The kickoff function is not available in crewai.crew.")

#test
