from __future__ import annotations
from typing import Any, Dict, List, Optional, Set

from backend.app.knowledge_base.career_mapping import get_required_skills_for_career
from backend.app.knowledge_base.skill_taxonomy import canonicalize_skill_name


def normalize_skill(raw_skill: Optional[str]) -> str:
    """Normalize a raw skill string to its canonical taxonomy form."""
    if raw_skill is None:
        return ''
    value = str(raw_skill).strip()
    if not value:
        return ''
    normalized = canonicalize_skill_name(value)
    return normalized if normalized else value.title()


def get_courses_for_skill(skill: str, max_courses: int = 3) -> List[Dict[str, Any]]:
    """Find top rated courses in the dataset that directly teach a given missing skill."""
    try:
        from backend.app.services.search_service import _load_processed_courses
        df = _load_processed_courses()
        skill_lower = skill.lower()
        
        # Match courses where skills or course_name contains the skill
        matches = []
        for _, row in df.iterrows():
            c_skills = str(row.get('skills', '')).lower()
            c_name = str(row.get('course_name', '')).lower()
            if skill_lower in c_skills or skill_lower in c_name:
                rating = float(row.get('rating') or 0.0)
                matches.append({
                    'course_id': str(row.get('course_id', '')),
                    'course_name': str(row.get('course_name', '')),
                    'difficulty': str(row.get('difficulty', 'Unknown')),
                    'rating': rating,
                    'organization': str(row.get('organization', '')),
                    'url': str(row.get('url', '')),
                })
        # Sort by rating descending
        matches.sort(key=lambda x: x['rating'], reverse=True)
        return matches[:max_courses]
    except Exception:
        return []


def get_skill_gap(
    current_skills: Optional[List[str]] = None,
    target_career: Optional[str] = None,
    target_skills: Optional[List[str]] = None,
    include_courses_for_missing: bool = True,
) -> Dict[str, Any]:
    """
    Perform skill-gap analysis comparing a student's current skill profile
    against target career requirements and target competencies.
    """
    raw_current = current_skills or []
    current_set: Set[str] = {normalize_skill(s) for s in raw_current if normalize_skill(s)}

    required_set: Set[str] = set()
    if target_career:
        for sk in get_required_skills_for_career(target_career):
            required_set.add(normalize_skill(sk))

    if target_skills:
        for sk in target_skills:
            norm = normalize_skill(sk)
            if norm:
                required_set.add(norm)

    # If no target career was provided, default to target_skills or empty
    if not required_set and current_set:
        # If user only specified current skills without career, recommend next-step skills
        required_set = set(current_set)

    existing = sorted(current_set & required_set)
    missing = sorted(required_set - current_set)

    coverage = round((len(existing) / len(required_set)) * 100, 1) if required_set else 100.0

    result: Dict[str, Any] = {
        'current_skills': sorted(current_set),
        'required_skills': sorted(required_set),
        'existing_skills': existing,
        'missing_skills': missing,
        'coverage_percentage': coverage,
        'target_career': target_career or 'General',
    }

    if include_courses_for_missing and missing:
        missing_courses_map = {}
        for m_skill in missing:
            courses = get_courses_for_skill(m_skill, max_courses=2)
            if courses:
                missing_courses_map[m_skill] = courses
        result['missing_skills_courses'] = missing_courses_map

    return result
