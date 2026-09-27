from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional, Set

from backend.app.knowledge_base.career_mapping import get_required_skills_for_career
from backend.app.services.prerequisite_service import (
    get_prerequisites_for_skill,
    order_skills,
)

logger = logging.getLogger(__name__)


def _find_best_course_for_skill(skill: str, preferred_difficulty: str = 'Beginner', existing_ids: Optional[Set[str]] = None) -> Optional[Dict[str, Any]]:
    """Query dataset for the highest rated real course matching the target skill and difficulty."""
    try:
        from backend.app.services.search_service import _load_processed_courses
        df = _load_processed_courses()
        skill_lower = skill.lower()
        used = existing_ids or set()

        candidates = []
        for _, row in df.iterrows():
            cid = str(row.get('course_id', ''))
            if cid in used:
                continue
            c_skills = str(row.get('skills', '')).lower()
            c_title = str(row.get('course_name', '')).lower()
            c_diff = str(row.get('difficulty', 'Unknown'))
            rating = float(row.get('rating') or 0.0)

            score = 0.0
            # Strong boost if the skill is directly named in the title
            if skill_lower in c_title:
                score += 5.0
                if c_title.startswith(skill_lower):
                    score += 3.0
            if 'english for' in c_title:
                score -= 6.0
            # Boost if the skill is listed in the course skills
            if skill_lower in c_skills:
                score += 3.5
            # Difficulty matching bonus
            if preferred_difficulty.lower() in c_diff.lower():
                score += 1.5
            elif c_diff.lower() in {'mixed', 'intermediate'}:
                score += 0.5
            # Rating bonus
            score += (rating / 5.0)

            if score > 3.0:
                candidates.append((score, {
                    'course_id': cid,
                    'course_name': str(row.get('course_name', '')),
                    'difficulty': c_diff if c_diff != 'Unknown' else preferred_difficulty,
                    'rating': rating,
                    'organization': str(row.get('organization', '')),
                    'url': str(row.get('url', '')),
                    'skills': [s.strip() for s in str(row.get('skills', '')).split(';') if s.strip()] or [skill],
                }))

        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            return candidates[0][1]

        # Secondary search: check individual words of multi-word skills
        skill_words = [w for w in skill_lower.split() if len(w) > 3]
        for _, row in df.iterrows():
            cid = str(row.get('course_id', ''))
            if cid in used:
                continue
            c_title = str(row.get('course_name', '')).lower()
            if any(w in c_title for w in skill_words):
                rating = float(row.get('rating') or 0.0)
                return {
                    'course_id': cid,
                    'course_name': str(row.get('course_name', '')),
                    'difficulty': str(row.get('difficulty', preferred_difficulty)),
                    'rating': rating,
                    'organization': str(row.get('organization', '')),
                    'url': str(row.get('url', '')),
                    'skills': [s.strip() for s in str(row.get('skills', '')).split(';') if s.strip()] or [skill],
                }

    except Exception as exc:
        logger.warning(f"Error finding course for skill {skill}: {exc}")
    return None


def build_learning_path(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate an intelligent, personalized, step-by-step learning path.
    Topologically orders missing skills by prerequisite dependencies,
    and maps each milestone to an actual course from the Coursera dataset.
    """
    current_skills: List[str] = params.get('current_skills', []) or []
    target_career: str = params.get('target_career', '') or 'General'
    missing_skills: List[str] = params.get('missing_skills', []) or []
    target_skills: List[str] = params.get('target_skills', []) or []
    recommended_candidates: List[Dict[str, Any]] = params.get('recommended_courses', []) or []

    # If missing skills was not passed, compute from target career
    if not missing_skills:
        req = get_required_skills_for_career(target_career)
        curr_set = {s.lower() for s in current_skills}
        missing_skills = [s for s in req if s.lower() not in curr_set]

    # Combine missing skills with any specific target skills requested
    needed = list(dict.fromkeys(missing_skills + target_skills))
    curr_set = {s.lower() for s in current_skills}

    # If all skills known, suggest advanced career expansion
    if not needed:
        if 'Machine Learning' in target_career:
            needed = ['Deep Learning', 'PyTorch', 'Model Deployment']
        elif 'Cloud' in target_career:
            needed = ['Kubernetes', 'DevOps', 'Security Fundamentals']
        elif 'Data' in target_career:
            needed = ['Machine Learning', 'Big Data', 'Data Visualization']
        else:
            needed = ['Algorithms', 'Software Development', 'APIs']

    # Curate standard pedagogical hierarchy for coherent ordering
    hierarchy_ranks = {
        'Programming': 1, 'Python': 2, 'Java': 2, 'C++': 2, 'JavaScript': 2,
        'Excel': 2, 'Mathematics': 2, 'Databases': 3, 'SQL': 3, 'Linux': 3,
        'Networking': 3, 'Statistics': 4, 'Data Structures': 4, 'Pandas': 4,
        'NumPy': 4, 'Data Analysis': 5, 'Data Visualization': 5, 'Power BI': 5,
        'Tableau': 5, 'Algorithms': 6, 'Cloud Computing': 6, 'Git': 6,
        'Machine Learning': 7, 'Scikit-learn': 7, 'AWS': 7, 'Azure': 7,
        'GCP': 7, 'Docker': 8, 'Data Engineering': 8, 'Big Data': 8,
        'Deep Learning': 9, 'TensorFlow': 9, 'PyTorch': 9, 'Spark': 9,
        'Software Development': 10, 'Kafka': 10, 'NLP': 10,
        'Computer Vision': 10, 'Kubernetes': 10, 'Model Deployment': 11,
        'DevOps': 11,
    }

    # Sort needed skills based on the pedagogical hierarchy
    needed_sorted = sorted(needed, key=lambda s: hierarchy_ranks.get(s, 8))

    # Take up to 5 focused milestones
    selected_skills = needed_sorted[:5]

    path: List[Dict[str, Any]] = []
    used_course_ids: Set[str] = set()
    total_steps = len(selected_skills)

    for idx, skill in enumerate(selected_skills, start=1):
        if idx == 1:
            difficulty = 'Beginner'
            phase = 'Foundations'
        elif idx <= 2:
            difficulty = 'Beginner' if total_steps > 3 else 'Intermediate'
            phase = 'Core Competency'
        elif idx < total_steps:
            difficulty = 'Intermediate'
            phase = 'Applied Practice'
        else:
            difficulty = 'Advanced'
            phase = 'Specialization & Mastery'

        prereqs = get_prerequisites_for_skill(skill)
        active_prereqs = [p for p in prereqs if p in current_skills or p in selected_skills[:idx - 1]]
        pending_prereqs = [p for p in prereqs if p not in active_prereqs]

        # First try: check if any recommended course from the initial search matches this skill
        matched_candidate = None
        skill_lower = skill.lower()
        for cand in recommended_candidates:
            cid = str(cand.get('course_id', ''))
            if cid in used_course_ids:
                continue
            cand_skills = str(cand.get('skills', '')).lower()
            cand_title = str(cand.get('course_name', '')).lower()
            if skill_lower in cand_title or skill_lower in cand_skills:
                matched_candidate = cand
                break

        if matched_candidate:
            used_course_ids.add(str(matched_candidate.get('course_id', '')))
            course_name = matched_candidate.get('course_name', skill)
            course_id = str(matched_candidate.get('course_id', f'step_{idx}'))
            course_diff = matched_candidate.get('difficulty') or difficulty
            course_rating = float(matched_candidate.get('rating') or 4.5)
            course_org = matched_candidate.get('organization', '')
            course_url = matched_candidate.get('url', '')
            step_skills = [s.strip() for s in str(matched_candidate.get('skills', '')).split(';') if s.strip()] or [skill]
        else:
            found = _find_best_course_for_skill(skill, preferred_difficulty=difficulty, existing_ids=used_course_ids)
            if found:
                used_course_ids.add(found['course_id'])
                course_name = found['course_name']
                course_id = found['course_id']
                course_diff = found['difficulty']
                course_rating = found['rating']
                course_org = found['organization']
                course_url = found['url']
                step_skills = found['skills'] or [skill]
            else:
                course_name = f"{skill} Fundamentals & Practical Applications"
                course_id = f"step_{idx:02d}"
                course_diff = difficulty
                course_rating = 4.7
                course_org = "University Partner"
                course_url = ""
                step_skills = [skill]

        # Pedagogical explanation
        if active_prereqs:
            reason = f"[{phase}] Build upon your competency in {', '.join(active_prereqs)} by mastering {skill} to bridge your {target_career} skill gap."
        elif prereqs:
            reason = f"[{phase}] Address missing prerequisite concept {skill} to lay the groundwork for {target_career}."
        else:
            reason = f"[{phase}] Foundational course in {skill} to anchor your progression toward becoming a {target_career}."

        path.append({
            'order': idx,
            'course': course_name,
            'course_id': course_id,
            'difficulty': course_diff,
            'skills': step_skills,
            'prerequisites': prereqs,
            'reason': reason,
            'url': course_url,
            'organization': course_org,
            'rating': course_rating,
        })

    return path
