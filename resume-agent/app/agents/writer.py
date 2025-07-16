from crewai import Agent
from langchain_community.chat_models import ChatLiteLLM
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPEN_ROUTER_API_KEY")

def writer_agent():
    model = ChatLiteLLM(
        model="openrouter/mistralai/mistral-7b-instruct",
        api_key=api_key,
        api_base="https://openrouter.ai/api/v1",
        temperature=0.5,
    )

    return Agent(
        role="Resume Writer",
        goal=(
            "Write optimized resume bullet points that clearly showcase the candidate's technical skills, measurable achievements, "
            "and unique contributions — using the extracted structured data and JD context."
        ),
        backstory=(
            "You're an expert technical resume writer. Your task is to rewrite raw project/experience details into polished, professional, "
            "ATS-friendly bullet points that align with the job description and hiring trends. Each section must be specific, crisp, and unique."
        ),
        output_format=(
            "Return JSON in this strict format:\n"
            "{\n"
            "  'optimized_resume': {\n"
            "    'title': 'Optimized Resume Bullet Points',\n"
            "    'sections': [\n"
            "      {\n"
            "        'heading': str,  // Usually the title or role + company\n"
            "        'points': [\n"
            "          str,  // Bullet point 1\n"
            "          str,  // Bullet point 2\n"
            "          str   // Bullet point 3\n"
            "        ]\n"
            "      }, ...\n"
            "    ]\n"
            "  }\n"
            "}\n"
            "Constraints:\n"
            "- Output EXACTLY 3 bullet points per section\n"
            "- Each point must highlight a unique technical contribution or measurable result\n"
            "- Do NOT copy input lines directly — rewrite them concisely and technically\n"
            "- Avoid repetition between sections\n"
            "- Use tools and metrics where possible (e.g. 'improved performance by 30%', 'used SQL/Power BI')"
        ),
        llm=model,
        verbose=True
    )
