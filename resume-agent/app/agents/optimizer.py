from crewai import Agent
from langchain_community.chat_models import ChatLiteLLM
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPEN_ROUTER_API_KEY")

def optimizer_agent():
    model = ChatLiteLLM(
    model="openrouter/mistralai/mistral-7b-instruct",
    api_key=api_key,
    api_base="https://openrouter.ai/api/v1",
    temperature=0.6
    )

    return Agent(
        role="Resume Optimizer",
        goal="Identify how each project or experience from the resume aligns with the job description, including gaps.",
        backstory="Specialist in aligning candidate background with job expectations and surfacing strengths and weaknesses.",
        llm=model,
        verbose=True
    )