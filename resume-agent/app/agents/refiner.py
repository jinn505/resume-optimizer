from crewai import Agent
from langchain_community.chat_models import ChatLiteLLM
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPEN_ROUTER_API_KEY")

def refiner_agent():
    model = ChatLiteLLM(
    model="openrouter/mistralai/mistral-7b-instruct",
    api_key=api_key,
    api_base="https://openrouter.ai/api/v1",
    temperature=0.6
    )

    return Agent(
        role="Resume Refiner",
        goal=(
            "Refine resume bullet points to maximize clarity, impact, and alignment with the job description."
        ),
        backstory=(
            "You're an expert resume consultant who specializes in polishing bullet points. "
            "You improve phrasing, strengthen action verbs, and ensure every bullet reflects key job description terms. "
            "Your focus is to subtly rephrase and enhance each point while preserving structure and meaning."
        ),
        llm=model,
        verbose=True,
    )