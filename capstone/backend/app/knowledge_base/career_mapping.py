CAREER_SKILLS = {
    'Data Analyst': ['SQL', 'Excel', 'Python', 'Pandas', 'Statistics', 'Data Visualization', 'Power BI'],
    'Data Scientist': ['Python', 'SQL', 'Statistics', 'Pandas', 'NumPy', 'Machine Learning', 'Data Visualization'],
    'Machine Learning Engineer': ['Python', 'Machine Learning', 'Deep Learning', 'Scikit-learn', 'TensorFlow', 'Mathematics', 'Model Deployment'],
    'Cloud Engineer': ['Cloud Computing', 'AWS', 'Azure', 'GCP', 'Linux', 'Networking', 'Docker', 'DevOps'],
    'Software Developer': ['Programming', 'Data Structures', 'Algorithms', 'Git', 'APIs', 'Databases', 'Software Development'],
    'Software Engineer': ['Programming', 'Data Structures', 'Algorithms', 'Git', 'APIs', 'Databases', 'Software Development', 'Object-Oriented Design', 'System Design'],
    'Data Engineer': ['Python', 'SQL', 'Big Data', 'Spark', 'Kafka', 'Data Engineering', 'Cloud Computing'],
    'Machine Learning': ['Python', 'Machine Learning', 'Statistics', 'Pandas', 'NumPy', 'Scikit-learn']
}

CAREER_ALIASES = {
    'data science': 'Data Scientist',
    'data scientist': 'Data Scientist',
    'machine learning engineer': 'Machine Learning Engineer',
    'ml engineer': 'Machine Learning Engineer',
    'cloud computing': 'Cloud Engineer',
    'cloud engineer': 'Cloud Engineer',
    'cloud engineering': 'Cloud Engineer',
    'cloud': 'Cloud Engineer',
    'software developer': 'Software Developer',
    'software engineer': 'Software Engineer',
    'software engineering': 'Software Engineer',
    'software enginner': 'Software Engineer',
    'enginner': 'Software Engineer',
    'developer': 'Software Developer',
    'data analyst': 'Data Analyst',
    'analyst': 'Data Analyst',
    'data engineer': 'Data Engineer'
}


def get_career_target(query: str) -> str | None:
    lowered = query.lower().strip()
    lowered = lowered.replace('enginner', 'engineer')
    lowered = lowered.replace('engginner', 'engineer')
    for key, value in CAREER_ALIASES.items():
        if key in lowered:
            return value
    return None


def get_required_skills_for_career(career: str):
    return CAREER_SKILLS.get(career, [])
