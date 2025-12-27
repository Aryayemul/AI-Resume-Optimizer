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

@app.post("/test_upload")
async def test_upload(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb+") as f:
        f.write(await file.read())

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(file_path)

    parsed_text = resume_parse(text)

    return {"parsed_text":parsed_text}


@app.post("/ats")
async def ats_api(
    file: UploadFile = File(...),
    job_decription: str = Form(None)
    ):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb+") as f:
        f.write(await file.read())

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(file_path)

    parsed_text = resume_parse(text)
    resume_string = parsed_to_text(parsed_text)

    #Auto generate job description if not provided


    #Claculate ATS Score
    ats_result = ats_score(resume_string, job_decription,JINA_API_KEY)

    return {
        "parsed_text": parsed_text,
        "job_description":job_decription,
        "ats_score":ats_result
    }








@app.post("/enhance_resume")
async def enhance_resume_api(
    file: UploadFile = File(...),
    job_decription: str = Form(None)
    ):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb+") as f:
        f.write(await file.read())

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(file_path)

    parsed_text = resume_parse(text)
    resume_string = parsed_to_text(parsed_text)

    #Auto generate job description if not provided


    #Claculate ATS Score
    ats_result = ats_score(resume_string, job_decription,JINA_API_KEY)

    enhanced_raw = enhance_resume(parsed_text, job_decription)
    enhanced_raw = enhanced_raw.removeprefix("```").removesuffix("```")

    enhanced_resume = json.loads(enhanced_raw)
    return {
        "parsed_text": parsed_text,
        "job_description":job_decription,
        "ats_score":ats_result,
        "enhanced_resume":enhanced_resume
    }



@app.post("/build_resume_pdf")
async def build_resume_pdf(
    file: UploadFile = File(...),
    job_description: str = Form(None)
):
    # Save file
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb+") as f:
        f.write(await file.read())

    # Extract
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_docx(file_path)

    # Parse
    parsed_text = resume_parse(text)
    resume_string = parsed_to_text(parsed_text)
    ats_result_before = ats_score(resume_string, job_description,JINA_API_KEY)
    # Auto JD
    if not job_description:
        job_description = auto_generate_job_description(resume_string, GROQ_API_KEY)

    # Enhance
    enhanced_raw = enhance_resume(parsed_text, job_description)
    enhanced_raw = enhanced_raw.strip("```")
    enhanced_resume = json.loads(enhanced_raw)
    enhanced_string = build_enhanced_string(enhanced_resume)
    ats_result_after = ats_score(enhanced_string, job_description, JINA_API_KEY)
    # Auto template selection
    template_id = select_template(parsed_text, job_description)
    template_path = get_template_path(template_id)

    context = enhanced_to_template_context(
        enhanced_resume,
        parsed_text
    )

    filled_tex = f"output_template_{template_id}.tex"

    fill_latex_template(template_path, context, filled_tex)

    pdf_path = build_pdf(filled_tex)
   
    return {
        "template_used": template_id,
        "ats_score":ats_result_before,
        "pdf_path": pdf_path,
        "ats_score_after":ats_result_after
    }




# pdf_path = r"C:\Users\DELL\vs_code\Ai_resume_Ats\Arya_Resume.pdf"
# pdf_text = extract_text_from_pdf(pdf_path)
# print("PDF text extracted\n",pdf_text[:500])

# parsed_pdf = resume_parse(pdf_text)
# print("\nParsed test\n",parsed_pdf)

