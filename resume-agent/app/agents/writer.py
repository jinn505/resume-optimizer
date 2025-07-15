from crewai import Agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

def writer_agent():
    model = ChatGroq(
     model="groq/llama-3.1-8b-instant",
     api_key= api_key,
     temperature = 0.6,
    )
    return Agent(
        role="Resume Writer",
        goal=(
            "Given the resume analysis and job description match data, return optimized resume bullet points. "
            "Each section should represent one project, internship, or experience, and contain exactly 3 bullet points that are crisp and technically aligned with the job description."
        ),
        backstory=(
            "An expert in writing resumes that align with job descriptions. You help convert raw resume content "
            "into grouped bullet points that match each work/project experience clearly."
        ),
        llm=model,
        verbose=True,
        output_format=(
            "Return JSON structured as:\n"
            "{ 'optimized_resume': { 'title': string, 'sections': [ "
            "{ 'heading': string, 'points': [string, string, string] }, ... ] } }.\n"
            "Avoid dumping raw resume JSON. Only return job/project titles and 3 crisp bullet points per section."
        )
    )
