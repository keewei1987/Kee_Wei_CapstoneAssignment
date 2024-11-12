import streamlit as st

st.title("🎈Methodology")
st.write(
    "A comprehensive explanation of the data flows and implementation details./n A flowchart illustrating the process flow for each of the use cases in the application. For example, if the application has two main use cases: a) chat with information and b) intelligent search, each of these use cases should have its own flowchart.")

st.header("Agents")
st.markdown('''
Data from: www.mom.gov.sg  
- Agent Planner  
- Agent Writer  
- Agent Research  
- Coding Agent  
- Agent Customer Service  
- Agent Complier  
''')

st.header("Successful Implementation")
st.markdown('''
- OPENAI Key made Secret  
- Password protected app  
- Incorporated error handling (try and except)
- Streamlit prompt powered by Crewai  
- Preset prompt at prompt widget for suggested prompt
- Streamlit powered OT calculator  
''')

import streamlit as st
import graphviz

# Title of the Streamlit app
st.title("CrewAI Agents and Tasks Flowchart")

# Create the Graphviz flowchart
flowchart = graphviz.Digraph(comment="CrewAI Agents and Tasks")

# Define agents
agents = {
    "agent_planner": "Content Planner",
    "agent_writer": "Content Writer",
    "agent_researcher": "Research Analyst",
    "agent_customerservice": "Customer Service Manager",
    "coding_agent": "Python Data Analyst",
    "agent_compiler": "Compiler"
}

# Define tasks and link them to agents
tasks = {
    "task_plan": "Planning Task",
    "task_research": "Research Task",
    "task_customerresponse": "Customer Response Task",
    "data_analysis_task": "Data Analysis Task",
    "task_summary": "Summary Task",
    "task_write": "Writing Task"
}

# Add agents as nodes in the flowchart
for agent_key, agent_label in agents.items():
    flowchart.node(agent_key, agent_label)

# Add tasks and connect them to agents
task_connections = {
    "task_plan": "agent_planner",
    "task_research": "agent_researcher",
    "task_customerresponse": "agent_customerservice",
    "data_analysis_task": "coding_agent",
    "task_summary": "agent_compiler",
    "task_write": "agent_writer"
}

# Define task dependencies (for visualizing task order)
dependencies = [
    ("task_plan", "task_research"),
    ("task_research", "task_write"),
    ("task_plan", "task_summary"),
    ("data_analysis_task", "task_research")
]

# Add task nodes and connect them to the corresponding agents
for task_key, agent_key in task_connections.items():
    flowchart.node(task_key, tasks[task_key], shape="box")
    flowchart.edge(agent_key, task_key)

# Add dependencies (task-to-task edges) to show flow between tasks
for task_from, task_to in dependencies:
    flowchart.edge(task_from, task_to, label="depends on")

# Render the flowchart in Streamlit
st.graphviz_chart(flowchart)
