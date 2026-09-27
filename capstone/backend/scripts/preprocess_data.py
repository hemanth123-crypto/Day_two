import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.config import BASE_DIR, PROCESSED_DIR
from backend.app.database import Base, engine, SessionLocal
from backend.app.knowledge_base.skill_taxonomy import canonicalize_skill_name
from backend.app.models.course import Course
from backend.app.utils.text_utils import normalize_space, safe_float

RAW_FILE = BASE_DIR / 'data' / 'raw' / 'courses.csv'
OUTPUT_FILE = PROCESSED_DIR / 'courses_cleaned.csv'


def clean_text_encoding(text: str) -> str:
    """Normalize text encoding and clean up corrupted characters or non-standard symbols."""
    if not isinstance(text, str):
        return ''
    cleaned = text
    # Clean common Coursera csv mojibake artifacts
    replacements = {
        '(ISC)\uFFFD': '(ISC)2',
        '(ISC)\ufffd': '(ISC)2',
        '(ISC)': '(ISC)2',
        '(ISC)A': '(ISC)2',
        '\ufffd': ' ',
    }
    for bad, good in replacements.items():
        if bad:
            cleaned = cleaned.replace(bad, good)
    # Decompose accented characters to clean ASCII representations for broad compatibility
    norm = unicodedata.normalize('NFKD', cleaned)
    ascii_text = norm.encode('ascii', 'ignore').decode('ascii')
    result = normalize_space(ascii_text)
    return result if result else normalize_space(cleaned)


def normalize_difficulty(value):
    if pd.isna(value):
        return 'Unknown'
    text = str(value).strip().lower()
    if 'begin' in text:
        return 'Beginner'
    if 'intermed' in text:
        return 'Intermediate'
    if 'adv' in text:
        return 'Advanced'
    if 'mixed' in text:
        return 'Intermediate'
    return text.title() if text else 'Unknown'


def normalize_rating(value):
    if pd.isna(value):
        return None
    text = str(value).strip()
    if text.lower() in {'na', 'n/a', 'none', ''}:
        return None
    try:
        return round(float(text), 2)
    except ValueError:
        try:
            cleaned = text.replace(',', '')
            return round(float(cleaned), 2)
        except ValueError:
            return None


def normalize_course_name(value):
    if pd.isna(value):
        return 'Unknown Course'
    return clean_text_encoding(value)


def normalize_skills(value):
    if pd.isna(value):
        return '[]'
    if isinstance(value, list):
        skills = value
    elif isinstance(value, str):
        skills = [part.strip() for part in re.split(r'[;,|/]+', value) if part.strip()]
    else:
        skills = [str(value)]
    norm = []
    for skill in skills:
        clean_s = clean_text_encoding(skill)
        canonical = canonicalize_skill_name(clean_s)
        if canonical:
            norm.append(canonical)
    return '; '.join(dict.fromkeys(norm))


def infer_skills_from_title(title):
    text = str(title or '').lower()
    inferred = []

    keyword_map = {
        'python': ['Python'],
        'machine learning': ['Machine Learning'],
        'deep learning': ['Deep Learning', 'Machine Learning'],
        'artificial intelligence': ['Artificial Intelligence'],
        'ai': ['Artificial Intelligence'],
        'data science': ['Data Analysis', 'Statistics', 'Python'],
        'data analysis': ['Data Analysis', 'Statistics'],
        'analytics': ['Data Analysis', 'Statistics'],
        'cloud': ['Cloud Computing', 'Security Fundamentals'],
        'aws': ['Cloud Computing', 'AWS'],
        'azure': ['Cloud Computing', 'Azure'],
        'gcp': ['Cloud Computing', 'GCP'],
        'docker': ['Docker', 'DevOps'],
        'kubernetes': ['Kubernetes', 'Cloud Computing'],
        'security': ['Security Fundamentals', 'Risk Management'],
        'database': ['Databases', 'SQL'],
        'sql': ['SQL', 'Databases'],
        'statistics': ['Statistics', 'Data Analysis'],
        'mathematics': ['Mathematics'],
        'linear algebra': ['Mathematics'],
        'programming': ['Programming'],
        'algorithms': ['Algorithms', 'Data Structures'],
        'data structures': ['Data Structures', 'Algorithms'],
        'software development': ['Software Development', 'Programming'],
        'software engineering': ['Software Engineering', 'Programming'],
        'web': ['Web Development', 'JavaScript'],
        'java': ['Java', 'Programming'],
        'c++': ['C++', 'Programming'],
    }

    for keyword, skills in keyword_map.items():
        if keyword in text:
            inferred.extend(skills)

    if not inferred:
        inferred = ['Critical Thinking', 'Research', 'Communication']

    normalized = []
    for skill in inferred:
        canonical = canonicalize_skill_name(skill)
        if canonical:
            normalized.append(canonical)
    return '; '.join(dict.fromkeys(normalized))


def infer_description_from_title(title):
    text = clean_text_encoding(str(title or ''))
    lower = text.lower()

    if 'data science' in lower or 'data analysis' in lower or 'analytics' in lower:
        return f"{text} introduces learners to the foundations of data analysis, statistical reasoning, and practical decision-making using real-world data examples."
    if 'machine learning' in lower or 'artificial intelligence' in lower or 'ai' in lower:
        return f"{text} helps learners understand core concepts, algorithms, and applications used in modern machine learning and intelligent systems."
    if 'deep learning' in lower or 'neural network' in lower:
        return f"{text} covers neural network architectures, backpropagation, and practical deep learning implementation."
    if 'cloud' in lower or 'aws' in lower or 'azure' in lower or 'security' in lower:
        return f"{text} covers the core ideas behind cloud-native systems, security principles, and the practical systems thinking needed to build and maintain modern digital services."
    if 'software' in lower or 'programming' in lower or 'developer' in lower:
        return f"{text} guides learners through software engineering patterns, algorithmic problem solving, and effective coding practices."
    return f"{text} introduces learners to the core ideas, foundational methods, and practical applications of this subject through guided study and applied examples."


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    columns = {str(col).strip().lower().replace(' ', '_').replace('-', '_'): col for col in df.columns}
    column_mapping = {
        'course_id': ['course_id', 'id'],
        'course_name': ['course_title', 'title', 'course_name', 'name'],
        'description': ['description', 'course_description', 'summary', 'overview'],
        'skills': ['skills', 'skill', 'course_skills', 'tags'],
        'difficulty': ['difficulty', 'course_difficulty', 'level'],
        'rating': ['rating', 'course_rating', 'avg_rating'],
        'organization': ['organization', 'course_organization', 'provider', 'school'],
        'url': ['url', 'course_url', 'link'],
    }
    target = {}
    for internal_name, aliases in column_mapping.items():
        for alias in aliases:
            if alias in columns:
                target[internal_name] = columns[alias]
                break

    if 'course_name' not in target:
        target['course_name'] = df.columns[0]
    if 'description' not in target:
        target['description'] = 'description'
    if 'organization' not in target:
        target['organization'] = 'organization'
    if 'difficulty' not in target:
        target['difficulty'] = 'difficulty'
    if 'rating' not in target:
        target['rating'] = 'rating'

    mapped = df.rename(columns={value: key for key, value in target.items()}).copy()

    for field, default in {
        'course_name': 'Unknown Course',
        'description': '',
        'skills': '',
        'difficulty': 'Unknown',
        'rating': None,
        'organization': 'Unknown',
        'url': '',
    }.items():
        if field not in mapped.columns:
            mapped[field] = default

    mapped['course_id'] = [f'course_{idx:04d}' for idx in range(len(mapped))]
    mapped['course_name'] = mapped['course_name'].apply(normalize_course_name)
    mapped['description'] = mapped['description'].fillna('').apply(lambda x: clean_text_encoding(x) if isinstance(x, str) else '')
    mapped['description'] = mapped.apply(
        lambda row: row['description'] if str(row['description']).strip() else infer_description_from_title(row['course_name']),
        axis=1,
    )
    mapped['skills'] = mapped['skills'].fillna('').apply(normalize_skills)
    mapped['skills'] = mapped.apply(
        lambda row: row['skills'] if str(row['skills']).strip() else infer_skills_from_title(row['course_name']),
        axis=1,
    )
    mapped['difficulty'] = mapped['difficulty'].fillna('Unknown').apply(normalize_difficulty)
    mapped['rating'] = mapped['rating'].apply(normalize_rating)
    mapped['organization'] = mapped['organization'].fillna('Unknown').apply(clean_text_encoding)
    mapped['url'] = mapped['url'].fillna('')
    mapped['search_text'] = mapped.apply(
        lambda row: ' '.join([
            str(row.get('course_name', '')),
            str(row.get('description', '')),
            str(row.get('skills', '')),
            str(row.get('difficulty', '')),
            str(row.get('organization', '')),
        ]), axis=1)

    mapped['metadata'] = mapped.apply(lambda row: {
        'organization': row.get('organization', ''),
        'difficulty': row.get('difficulty', 'Unknown'),
        'rating': row.get('rating', None),
        'url': row.get('url', '')
    }, axis=1)

    cleaned = mapped[['course_id', 'course_name', 'description', 'skills', 'difficulty', 'rating', 'organization', 'url', 'search_text', 'metadata']].drop_duplicates(subset=['course_name', 'description']).reset_index(drop=True)
    return cleaned


def sync_to_sqlite(df: pd.DataFrame):
    """Sync cleaned course dataset to SQLite database table."""
    try:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        # Clear existing courses in SQLite table
        db.query(Course).delete()
        courses_to_add = []
        for _, row in df.iterrows():
            c = Course(
                course_id=str(row['course_id']),
                course_name=str(row['course_name']),
                description=str(row.get('description', '')),
                skills=str(row.get('skills', '')),
                difficulty=str(row.get('difficulty', 'Unknown')),
                rating=float(row['rating']) if pd.notna(row.get('rating')) else None,
                organization=str(row.get('organization', 'Unknown')),
                url=str(row.get('url', '')),
                search_text=str(row.get('search_text', '')),
            )
            courses_to_add.append(c)
        db.bulk_save_objects(courses_to_add)
        db.commit()
        db.close()
        print(f"Synced {len(courses_to_add)} courses into SQLite database table 'courses'")
    except Exception as exc:
        print(f"Warning: Could not sync to SQLite ({exc})")


def main():
    if not RAW_FILE.exists():
        raise FileNotFoundError(f'Course dataset not found at {RAW_FILE}. Download the CSV into data/raw/courses.csv.')
    df = pd.read_csv(RAW_FILE)
    cleaned = prepare_dataframe(df)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT_FILE, index=False)
    print(f'Cleaned dataset saved to {OUTPUT_FILE} ({len(cleaned)} courses)')
    sync_to_sqlite(cleaned)


if __name__ == '__main__':
    main()
