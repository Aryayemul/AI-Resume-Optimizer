def latex_escape(text):
    if not text:
        return ""
    return (
        text.replace("\\", r"\textbackslash{}")
            .replace("&", r"\&")
            .replace("%", r"\%")
            .replace("$", r"\$")
            .replace("#", r"\#")
            .replace("_", r"\_")
            .replace("{", r"\{")
            .replace("}", r"\}")
            .replace("~", r"\textasciitilde{}")
            .replace("^", r"\textasciicircum{}")
    )

def safe(text):
    return latex_escape(text) if text and text.strip() else ""



def section_block(title, content):
    if not content.strip():
        return ""
    return f"\\section*{{{title}}}\n{content}\n\\vspace{{6pt}}\n"


def enhanced_to_template_context(enhanced, parsed):
    return {
        "NAME": safe(parsed["personal_info"].get("name")),
        "EMAIL": safe(parsed["personal_info"].get("email")),
        "PHONE": safe(parsed["personal_info"].get("phone")),

        "SUMMARYBLOCK": section_block("Professional Summary", safe(enhanced.get("enhanced_summary",""))),
        "SKILLSBLOCK": section_block("Technical Skills", safe(enhanced.get("enhanced_skills",""))),
        "PROJECTSBLOCK": section_block("Project Experience", safe(enhanced.get("enhanced_projects",""))),
        "EXPERIENCEBLOCK": section_block("Professional Experience", safe(enhanced.get("enhanced_experience",""))),
        "EDUCATIONBLOCK": section_block("Education", safe(enhanced.get("enhanced_education",""))),
    }

