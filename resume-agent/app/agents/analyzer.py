from crewai import Agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

def analyzer_agent():
    model = ChatGroq(
     model="groq/llama-3.1-8b-instant",
     api_key= api_key,
     temperature = 0.6,
    )
    return Agent(
        role = "Resume Analyzer",
        goal="Extract all projects, internships, and work experiences from the resume into structured JSON format.",
        backstory="An expert in analyzing resumes and producing structured summaries that include projects, internships, and experience clearly categorized.",

        llm = model,
        verbose=True
    )