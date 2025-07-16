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
        model="openrouter/deepseek/deepseek-chat:free",  # 👈 Use this for better JSON output
        api_key=api_key,
        api_base="https://openrouter.ai/api/v1",
        temperature=0.4
    )

    return Agent(
        role="Resume and JD Extractor",
        goal="Extract structured project, experience, skills, and JD content into grouped JSON format.",
        backstory=(
            "You're a structured data extraction expert. You preserve every detail in grouped format. "
            "Your job is to extract experience, projects, and skills grouped under the correct titles. "
            "Each group must have exactly 3 bullet points — no more."
        ),
        output_format=(
            "Extract and return a valid JSON like:\n"
            "{\n"
            "  \"projects\": [\n"
            "    {\n"
            "      \"title\": str,\n"
            "      \"duration\": str or null,\n"
            "      \"tools\": [str],\n"
            "      \"description\": [str, str, str]  // exactly 3 bullet points\n"
            "    }\n"
            "  ],\n"
            "  \"experience\": [\n"
            "    {\n"
            "      \"role\": str,\n"
            "      \"company\": str,\n"
            "      \"duration\": str or null,\n"
            "      \"tools\": [str],\n"
            "      \"responsibilities\": [str, str, str]  // exactly 3 bullet points\n"
            "    }\n"
            "  ],\n"
            "  \"skills\": [str],\n"
            "  \"education\": [str],\n"
            "  \"certifications\": [str],\n"
            "  \"jd\": {\n"
            "    \"requirements\": [str],\n"
            "    \"responsibilities\": [str],\n"
            "    \"bonus\": [str]\n"
            "  }\n"
            "}\n\n"
            "Rules:\n"
            "- For projects and experience, group ALL related bullet points under that item (don't split).\n"
            "- Pick exactly 3 most important/resume-worthy points per project/experience (if more exist).\n"
            "- Only extract what's present in the input — don't summarize, rephrase, or invent content.\n"
            "- Always return valid JSON with no extra text or explanation.\n"
        ),
        llm=model,
        verbose=True
    )
