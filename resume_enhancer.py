from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def enhance_resume(parsed_resume, job_description):
    prompt = f"""
You are an expert ATS resume optimizer.

Your task is to enhance the resume content WITHOUT changing its structure or removing any information.

Rules:
1. Improve grammar, clarity, and professional tone.
2. Rewrite content to be ATS-friendly using strong action verbs.
3. Optimize keywords based on the provided job description.
4. Do NOT add fake experience, education, or skills.
5. Do NOT remove or shorten any section.
6. Preserve all original sections and enhance their full content.
7. Keep responsibilities, achievements, and timelines intact.

Job Description:
{job_description}

Parsed Resume (JSON):
{parsed_resume}

Return ONLY valid raw JSON.
Do NOT include markdown.
Do NOT include backticks.
Do NOT include explanations.

Return ONLY valid JSON in the following format (no markdown, no explanation):

{{
  "enhanced_summary": "",
  "enhanced_experience": "",
  "enhanced_education": "",
  "enhanced_skills": "",
  "enhanced_projects": "",
  "suggested_keywords": [],
  "improvement_suggestions": []
}}
"""


    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an ATS resume optimization expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content
