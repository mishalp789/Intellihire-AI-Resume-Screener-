def calculate_match_score(resume_text, job_required_skills):
    resume_words = set(resume_text.lower().split())
    job_skills = set(job_required_skills.lower().split(','))
    job_skills = {skill.strip() for skill in job_skills}

    matched = resume_words.intersection(job_skills)
    if not job_skills:
        return 0
    return round((len(matched) / len(job_skills)) * 100)
