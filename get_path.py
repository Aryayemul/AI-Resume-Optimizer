TEMPLATE_DIR = r"C:\Users\DELL\vs_code\Ai_resume_Ats\templates"

def get_template_path(template_id: int):
    templates = {
        1: f"{TEMPLATE_DIR}/template1.tex",
        2: f"{TEMPLATE_DIR}/template2.tex",
        3: f"{TEMPLATE_DIR}/template3.tex",
    }

    if template_id not in templates:
        raise ValueError("Invalid template ID")

    return templates[template_id]
