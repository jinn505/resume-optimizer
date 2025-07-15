import re
from typing import List, Dict

def format_resume_output(text: str) -> dict:
    # Remove markdown formatting
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    lines = [line.strip().lstrip("- ") for line in text.split("\n") if line.strip()]

    sections = []
    current_section = {"heading": "", "points": []}

    for line in lines:
        # Detect new section heading
        if not line.startswith(tuple("0123456789")) and not line.startswith("-"):
            if current_section["heading"]:
                sections.append(current_section)
            current_section = {"heading": line.rstrip(":"), "points": []}
        else:
            current_section["points"].append(line.rstrip(","))

    if current_section["heading"]:
        sections.append(current_section)

    return {
        "optimized_resume": {
            "title": "Optimized Resume Bullet Points",
            "sections": sections
        }
    }
