import pdfplumber
import docx
import re


def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text +=page.extract_text() + "\n"
    return text

def extract_text_from_docx(path):
    doc = docx.Document(path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_section(text,pattern,all_patterns):
    match = re.search(pattern,text,re.IGNORECASE)
    if not match:
        return ""
    
    start = match.end()

    #find the nearest next section
    next_positions = []
    for p in all_patterns:
        m = re.search(p,text[start:],re.IGNORECASE)
        if m:
            next_positions.append(m.start())

    end = start + min(next_positions) if next_positions else len(text)

    return text[start:end].strip()



# parseing basic details
def resume_parse(text):
    parsed = {
        "personal_info" : {},
        "summary" : "",
        "experience": [],
        "education" : [],
        "skills" : [],
        "projects" : []
    }

    #extract email
    email = re.findall(r"[A-Za-z0-9\._+-]+@[A-Za-z0-9\._-]+\.[A-Za-z]+",text)
    if email:
        parsed["personal_info"]["email"] = email[0]

    #Extract phone
    phone = re.findall(r"\+?\d[\d -]{8,}\d", text)
    if phone:
        parsed["personal_info"]["phone"] = phone[0]

    #nlp sections
    sections = {
    "experience": r"(experience|work history|employment)",
    "education": r"(education|academics)",
    "skills": r"(skills|technical skills)",
    "projects": r"(projects|personal projects|academic projects|work projects|project)"     
    }

    #patterns list for detecting next section
    all_patterns = list(sections.values())

    #extract each section
    for sec, pattern in sections.items():
            parsed[sec] = extract_section(text, pattern, all_patterns)

    return parsed
