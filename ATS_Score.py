import requests
import re

def clean_text(text):
    text = re.sub(r'\s+',' ',text)
    return text.strip()

def ats_score(resume_text, job_description, api_key):
    endpoint = "https://api.jina.ai/v1/rerank"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model":"jina-reranker-v1-base-en",
        "query":clean_text(job_description),
        "documents":[clean_text(resume_text)]
    }

    response = requests.post(endpoint, json=payload, headers = headers)

    if response.status_code !=200:
        return {
            "error":"API request failed",
            "details":response.text
        }
    
    score = response.json()["results"][0]["relevance_score"]

    #convert 0-1 float to ATS score (0-100)
    ats_score = round(score * 100, 2)

    return {
        "ats_score":ats_score,
        "match_quality":(
            "Excellent" if ats_score >= 80 else
            "Good" if ats_score >= 60 else
            "Average" if ats_score >= 40 else
            "Poor"
        )
    }
