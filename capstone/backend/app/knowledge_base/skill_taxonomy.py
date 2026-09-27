SKILL_ALIASES = {
    'python programming': 'Python',
    'python': 'Python',
    'py': 'Python',
    'sql': 'SQL',
    'java': 'Java',
    'c++': 'C++',
    'cpp': 'C++',
    'javascript': 'JavaScript',
    'react': 'React',
    'fastapi': 'FastAPI',
    'django': 'Django',
    'pandas': 'Pandas',
    'numpy': 'NumPy',
    'scikit-learn': 'Scikit-learn',
    'sklearn': 'Scikit-learn',
    'tensorflow': 'TensorFlow',
    'pytorch': 'PyTorch',
    'machine-learning': 'Machine Learning',
    'machine learning': 'Machine Learning',
    'ml': 'Machine Learning',
    'deep learning': 'Deep Learning',
    'artificial intelligence': 'Artificial Intelligence',
    'statistics': 'Statistics',
    'data analysis': 'Data Analysis',
    'data analytics': 'Data Analysis',
    'data visualization': 'Data Visualization',
    'power bi': 'Power BI',
    'tableau': 'Tableau',
    'excel': 'Excel',
    'cloud computing': 'Cloud Computing',
    'aws': 'AWS',
    'azure': 'Azure',
    'gcp': 'GCP',
    'docker': 'Docker',
    'kubernetes': 'Kubernetes',
    'git': 'Git',
    'github': 'GitHub',
    'nlp': 'NLP',
    'natural language processing': 'NLP',
    'computer vision': 'Computer Vision',
    'big data': 'Big Data',
    'spark': 'Spark',
    'kafka': 'Kafka',
    'data engineering': 'Data Engineering',
    'data engineering': 'Data Engineering',
    'programming': 'Programming',
    'algorithms': 'Algorithms',
    'data structures': 'Data Structures',
    'software development': 'Software Development',
    'api': 'APIs',
    'apis': 'APIs',
    'linux': 'Linux',
    'networking': 'Networking',
    'devops': 'DevOps',
    'mathematics': 'Mathematics',
    'model deployment': 'Model Deployment',
    'model serving': 'Model Deployment',
    'predictive analytics': 'Predictive Analytics',
    'regression': 'Regression',
    'classification': 'Classification',
    'database': 'Databases',
    'databases': 'Databases'
}

SKILL_TAXONOMY = sorted(set(SKILL_ALIASES.values()))


def canonicalize_skill_name(raw_skill: str) -> str:
    if raw_skill is None:
        return ''
    cleaned = str(raw_skill).strip()
    if not cleaned:
        return ''
    lowered = cleaned.lower().replace('_', ' ')
    return SKILL_ALIASES.get(lowered, cleaned.title())
