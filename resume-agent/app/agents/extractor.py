from crewai import Agent
from langchain_community.chat_models import ChatLiteLLM
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPEN_ROUTER_API_KEY")

def extractor_agent():
    model = ChatLiteLLM(
    model="openrouter/mistralai/mistral-7b-instruct",
    api_key=api_key,
    api_base="https://openrouter.ai/api/v1",
    temperature=0.6
    )

    return Agent(
        role="Extractor",
        goal="Extract all key structured details from resume and job description.",
        backstory=(
            "You are a parsing expert specializing in analyzing unstructured resume and JD text. "
            "Your task is to extract useful information like projects, experience, skills, tools, outcomes, and JD criteria."
        ),
        llm=model,
        verbose=True,
    )