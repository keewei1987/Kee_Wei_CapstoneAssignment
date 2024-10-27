import streamlit as st

st.title("🎈Methodology")
st.write(
    "A comprehensive explanation of the data flows and implementation details./n A flowchart illustrating the process flow for each of the use cases in the application. For example, if the application has two main use cases: a) chat with information and b) intelligent search, each of these use cases should have its own flowchart.")

st.header("Data Flows")
st.markdown('''
www.mom.gov.sg  
> Agent Planner  
> Agent Writer  
> Agent Research  
            > Coding Agent  
> Agent Customer Service  
> Agent Complier  
''')

st.header("Successful Implementation")
st.markdown('''
- OPENAI Key made Secret  
- Password protected app  
- Streamlit prompt powered by Crewai  
- Preset prompt at prompt widget for suggested prompt
- Streamlit powered OT calculator  
''')