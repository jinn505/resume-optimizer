from crewai import Agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

def optimizer_agent():
    model = ChatGroq(
     model="groq/llama-3.1-8b-instant",
     api_key= api_key,
     temperature = 0.6,
    )
    return Agent(
        role="Resume Optimizer",
        goal="Identify how each project or experience from the resume aligns with the job description, including gaps.",
        backstory="Specialist in aligning candidate background with job expectations and surfacing strengths and weaknesses.",
        llm=model,
        verbose=True
    )