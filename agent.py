from dotenv import load_dotenv
import os
import json
from groq import Groq
from fastapi import FastAPI, UploadFile, File, Form
from resume_parse import extract_text_from_pdf,extract_text_from_docx,resume_parse
from ATS_Score import ats_score
from dotenv import load_dotenv
from resume_enhancer import enhance_resume
from fill_latex_template import fill_latex_template
from context import enhanced_to_template_context
from template_selector import select_template
from get_path import get_template_path
from generate_pdf import build_pdf


load_dotenv()

JINA_API_KEY = os.getenv("JINA_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


app = FastAPI()

def parsed_to_text(parsed):
    text = ""
    
    if "personal_info" in parsed:
        for key, value in parsed["personal_info"].items():
            text += f"{key}: {value}\n"

    for section in ["summary", "experience", "education", "skills", "projects"]:
        if parsed.get(section):
            text += f"\n{section.upper()}:\n{parsed[section]}\n"
    
    return text


def auto_generate_job_description(parsed_text, groq_api_key):
    """
    Create a job description based on the user's resume if they didn't supply one.
    """
    client = Groq(api_key=groq_api_key)

    prompt = f"""
    The user uploaded a resume. Create a realistic job description that matches the user's experience.
    Resume content:
    {parsed_text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    return response.choices[0].message.content
def build_enhanced_string(enhanced):
    return f"""
SUMMARY:
{enhanced.get('enhanced_summary','')}

EXPERIENCE:
{enhanced.get('enhanced_experience','')}

SKILLS:
{enhanced.get('enhanced_skills','')}

PROJECTS:
{enhanced.get('enhanced_projects','')}

EDUCATION:
{enhanced.get('enhanced_education','')}
"""

class ResumeAgentState:
    INIT = "init"
    JD_GEN = "jd_generate"
    ATS_SCAN = "ats_scan"
    ENHANCE = "enhance"
    TEMPLATE = "template_select"
    BUILD = "build"
    COMPLETE = "complete"


def resume_agent_controller(parsed, jd):

    state = ResumeAgentState.INIT
    resume_text = parsed_to_text(parsed)

    if not jd:
        state = ResumeAgentState.JD_GEN
        jd = auto_generate_job_description(resume_text, GROQ_API_KEY)

    while True:
        state = ResumeAgentState.ATS_SCAN
        ats = ats_score(resume_text, jd, JINA_API_KEY)

        if ats["ats_score"] >= 80:
            break

        state = ResumeAgentState.ENHANCE
        enhanced = enhance_resume(parsed, jd)
        resume_text = enhanced

    state = ResumeAgentState.TEMPLATE
    template_id = select_template(parsed, jd)

    state = ResumeAgentState.BUILD
    build_pdf(enhanced, template_id)

    state = ResumeAgentState.COMPLETE

    return {
        "ats_final": ats,
        "template_used": template_id,
        "jd_used": jd
    }
