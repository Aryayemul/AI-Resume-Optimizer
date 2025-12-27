def select_template(parsed_resume: dict, job_description: str | None = None) -> int:
    """
    Automatically selects the best LaTeX resume template.
    Returns template_id (1, 2, or 3)
    """

    experience = parsed_resume.get("experience", "").strip()
    projects = parsed_resume.get("projects", "").strip()
    skills = parsed_resume.get("skills", "").lower()

    # Count signals
    has_experience = len(experience) > 120
    project_count = projects.count("\n") + 1 if projects else 0
    skill_count = len(skills.split(","))

    # ML / Data keywords
    tech_keywords = [
        "machine learning", "deep learning", "nlp", "computer vision",
        "tensorflow", "pytorch", "scikit", "data", "ai"
    ]

    tech_score = sum(1 for k in tech_keywords if k in skills)

    # 🎯 Decision Rules
    if has_experience and skill_count > 12:
        return 2  # Experienced Professional

    if tech_score >= 3 or project_count >= 3:
        return 3  # ML / Tech-heavy

    return 1  # Fresher / Student
