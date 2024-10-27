# Common imports
import os
from dotenv import load_dotenv
import json
import lolviz

#from langchain.agents import Tool
#from langchain.agents.agent_types import AgentType
#from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
#from langchain_openai import ChatOpenAI
#import pandas as pd

from interpreter import interpreter
from langchain.agents import Tool

# Set the model to use for the interpreter
interpreter.llm.model = "gpt-4o-mini"

# Create the tool
tool_coding = Tool(
    name="Python Code Interpreter",
    func=interpreter.chat, # <-- This is the function that will be called when the tool is run. Note that there is no `()` at the end
    description="Useful for running Python3 Code",
)


# Import the key CrewAI classes
#from helperfunctions.crewai 
from crewai import Agent, Task, Crew

from crewai_tools import WebsiteSearchTool
# Create a new instance of the WebsiteSearchTool
# Set the base URL of a website, e.g., "https://example.com/", so that the tool can search for sub-pages on that website
tool_websearch = WebsiteSearchTool(website="https://www.mom.gov.sg/")

# Creating Agents
# region <--------- Creating Agent --------->
agent_planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",

    backstory="""You're working on planning a response about the topic: {topic}."
    You decide how best to respond to the {topic}.
    You collect information that helps the audience learn something about the topic and make informed decisions.
    Make the best use of the agents and tools provided to gather the as much necessary information as possible.
    """,
    #Your response should strictly based on content from "https://www.mom.gov.sg/".
    #if the topic is out of scope, delegate to the task to agent_customerservice

    tools=[tool_websearch], #<--  This is the line that includes the tool
    allow_delegation=True, 
	verbose=True, 
)

agent_writer = writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate response about the topic: {topic}",
    backstory="""You're working on a writing a response about the topic: {topic}.""",

    allow_delegation=False, 
    verbose=True, 
)

agent_researcher = Agent(
    role="Research Analyst",
    goal="Conduct in-depth research on the topic: {topic}",
    backstory="""You're working on conducting in-depth research on the topic: {topic}.
    You have access to web search tools and other resources to gather the necessary information.
    You may also delegate the task to coding_agent to analyse tabular data if needed.
    """,

    allow_delegation=True,
    verbose=True,
)

agent_customerservice = Agent(
    role="Customer Service Manager",
    goal="Provide a professional yet firm response if {topic} is out of scope",
    backstory="""
    You are working on a professional response if the {topic} is out of the scope of the [tool_websearch].
    Kindly refer the user to check or submit enquiry via "www.mom.gov.sg".
    """,
    allow_delegation=False,
    verbose=True,
)

# Create an agent with code execution enabled
coding_agent = Agent(
    role="Python Data Analyst",
    goal="Analyze Tabular data and provide insights using Python",
    backstory="You are an experienced data analyst with strong Python skills.",

    #allow_code_execution=True,
    tools=[tool_coding],

    allow_delegation=False,
    verbose=True,
)

agent_compiler = Agent(
    role="Compiler",
    goal="Summarize the latest 5 {topic} and if needed do more research",
    backstory="You are a expert in compiling and summmarising the latest news",
    verbose=True,
)

# Creating Tasks
# region <--------- Creating Task --------->
task_plan = Task(
    description="""\
    
    1. Understand the requirements.
    2. Identify the correct approach to provide a response on {topic}.
    3. Delegate task to appropriate agent if needed.
    4. Respond based on content from "https://www.mom.gov.sg/".
    
    """,
    #4. Respond only on manpower-related topics on Work passes, employment practices, workplace safety and health, labour statistic and manpower-related publications and statistics.
    #5. if {topic} is irrelevant and not found on "https://www.mom.gov.sg/", do not proceed with any respond. Delegate the task to agent_customerservice.

    expected_output="""\
    A comprehensive response plan document with an outline, audience analysis, SEO keywords, and resources.""",
    agent=agent_planner,

    #async_execution=True # Will be executed asynchronously
)


# New Tasks (Research Task) to be performed by the Research Analyst
task_research = Task(
    description="""\
    1. Conduct in-depth research on the topic: {topic}.
    2. Provide the Content writer with the latest trends, key players, and noteworthy news on the topic.
    3. Provide additional insights and resources to enhance the content plan.
    4. Include latest developmnents in the research report.
    5. Prioritize the latest trends, key players, and noteworthy news on {topic}.
    6. Identify the target audience, considering "their interests and pain points.
    7. Develop a detailed content, including introduction, key points, and a call to action.
    """,

    expected_output="""\
    A detailed research report with the latest trends, key players, and noteworthy news on the topic.""",

    agent=agent_researcher,
    tools=[tool_websearch],

    #async_execution=True # Will be executed asynchronously
)

task_customerresponse = Task(
    description="""\
    1. Use the content plan to craft a professional reply on {topic} when it is out of scope.
    2. Kindly reject the {topic} that it is out of scope and refer user to to check or submit enquiry via "www.mom.gov.sg"
    3. Proofread for grammatical errors and alignment the common style.
    """,

    expected_output="""
    A short reply to ask user refer to MOM website for more info.""",
    
    agent=agent_customerservice,
    async_execution=False # Will be executed asynchronously
)

# Create a task that requires code execution
data_analysis_task = Task(
    description="""\
    1. Understand the user request on the requirements: {topic}.
    2. if {topic} consist tabular data, write code to analyze tabular dataset based on requirements.Proceed to next step only if the code is correct.
    3. Run the code and share the output.
    4. top iterating once the output is correct.
    5. Provide the researcher with the in-depth analysis on trends or any other insights.
    6. Provide additional insights and resources to enhance the content plan.
    """,

    agent=coding_agent,
    expected_output=""" Python dataframe for analysis """
)

task_summary = Task(
    description="a tldr summary of {topic} from MOM Newsroom",
    expected_output="compile latest 5 article in bullet point form with a short summary on {topic} from MOM Newsroom and provide url for each bullet point",
    
    agent= agent_compiler,
    context=[task_plan],
    async_execution=True # Will be executed asynchronously
)

task_write = Task(
    description="""\
    1. Use the content plan to craft a compelling response on {topic}.
    2. Sections/Subtitles are properly named in an engaging manner.
    3. Ensure the response is short and structured. Provide step-by-step if needed.
    4. Proofread for grammatical errors and alignment the common style used in tech blogs.
    
    """,
    #5. if content not found from "https://www.mom.gov.sg/", do not proceed. Delegate task to agent_customerservice.
    #5. Ensure that the content is from "https://www.mom.gov.sg/".
    
    expected_output="""
    A well-written response "in markdown format, ready for publication, each section should have 2 or 3 paragraphs.""",
    agent=agent_writer,
    #human_input=True

    context=[task_plan, task_research]# Will wait for the output of the two tasks to be completed,
)


# Creating the Crew
# region <--------- Creating Crew --------->
crew = Crew(
    agents=[agent_planner, agent_writer,agent_researcher,agent_customerservice,coding_agent,agent_compiler],
    tasks=[task_plan, task_research, task_summary, task_write],
    verbose=True,
    planning=True
)
