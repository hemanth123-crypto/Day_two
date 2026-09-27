from __future__ import annotations
import math
from typing import Any, Dict, List, Optional, Set

from backend.app.config import TOP_K
from backend.app.knowledge_base.career_mapping import get_required_skills_for_career
from backend.app.services.learning_path_service import build_learning_path
from backend.app.services.prerequisite_service import build_prerequisite_graph
from backend.app.services.query_parser import parse_user_query
from backend.app.services.ranking_service import hybrid_rank
from backend.app.services.search_service import search_courses
from backend.app.services.skill_service import get_skill_gap
from backend.app.services.llm_service import generate_rag_answer


def _json_safe(value: Any) -> Any:
    """Ensure floating points with NaN/Inf convert to valid JSON numbers or nulls."""
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return round(value, 4)
    return value


def _generate_explanation(
    item: Dict[str, Any],
    target_career: Optional[str],
    matched_skills: List[str],
    missing_skills: List[str],
    difficulty_pref: str,
) -> str:
    """
    Generate an educational, grounded explanation for why this course was recommended.
    Uses factual metadata (skills, organization, rating, difficulty) without hallucinations.
    """
    course_name = item.get('course_name', 'This course')
    org = item.get('organization') or 'top partner institutions'
    rating = item.get('rating')
    rating_str = f"with a {rating:.1f} rating" if rating and rating > 0 else "from recognized educators"
    diff = item.get('difficulty', 'Intermediate')

    reasons: List[str] = []

    # Career & skill alignment
    target_label = target_career if target_career else "your professional learning goal"
    if matched_skills:
        reasons.append(
            f"directly targets skills you need ({', '.join(matched_skills[:3])}) for {target_label}"
        )
    elif target_career:
        reasons.append(f"provides key competencies in the {target_label} domain")

    # Missing skill coverage
    covered_gaps = [s for s in matched_skills if s in missing_skills]
    if covered_gaps:
        reasons.append(f"helps close your identified skill gap in {', '.join(covered_gaps[:2])}")

    # Institutional quality & difficulty fit
    if difficulty_pref and difficulty_pref.lower() not in {'any', 'unknown'}:
        if difficulty_pref.lower() == diff.lower():
            reasons.append(f"matches your preferred {diff} difficulty level")
        else:
            reasons.append(f"offers {diff}-level structured curriculum")
    else:
        reasons.append(f"offers {diff}-level instruction provided by {org} ({rating_str})")

    if reasons:
        explanation = f"Recommended because it {' and '.join(reasons)}."
    else:
        explanation = f"Highly rated course ({rating_str}) by {org} covering relevant technical principles in this subject area."

    return explanation


def build_recommendations(
    query: str,
    top_k: int = TOP_K,
    current_skills: Optional[List[str]] = None,
    target_career: Optional[str] = None,
    preferred_difficulty: Optional[str] = None,
) -> Dict[str, Any]:
    """
    End-to-end recommendation workflow:
    1. Parse natural-language intent (existing skills, target career, domain, difficulty).
    2. Analyze skill gaps against target career competencies.
    3. Perform semantic retrieval using FAISS vector store.
    4. Calculate multi-factor hybrid score and rerank candidates.
    5. Construct dynamic prerequisite relationships.
    6. Generate a personalized, sequential learning path from real courses.
    """
    parsed = parse_user_query(query)

    # Use explicit parameter overrides if provided, otherwise parsed values
    current = current_skills if (current_skills is not None and len(current_skills) > 0) else parsed.get('existing_skills', [])
    effective_career = target_career or parsed.get('target_career')
    effective_diff = preferred_difficulty or parsed.get('difficulty', 'Any')

    # 1. Skill Gap Analysis
    skill_gap = get_skill_gap(
        current_skills=current,
        target_career=effective_career,
        target_skills=parsed.get('desired_skills', []),
        include_courses_for_missing=True,
    )

    required_skills = skill_gap.get('required_skills', [])
    missing_skills = skill_gap.get('missing_skills', [])

    # 2. Semantic Search with FAISS: Augment query with target intent and missing skills to retrieve goal-aligned courses
    target_intent_terms = []
    if effective_career:
        target_intent_terms.append(effective_career)
    if parsed.get('desired_skills'):
        target_intent_terms.extend(parsed.get('desired_skills'))
    if missing_skills:
        target_intent_terms.extend(missing_skills[:3])
    
    # Combined search query balances the natural language text with the target goals
    augmented_query = f"{query} {' '.join(target_intent_terms)}".strip()

    raw_results = search_courses(
        query=augmented_query,
        top_k=max(top_k * 3, 25),
        difficulty=effective_diff if effective_diff not in {'Any', 'all', ''} else None,
    )

    # 3. Score calculation for hybrid reranking
    career_skills_lower = {s.lower() for s in required_skills}
    missing_skills_lower = {s.lower() for s in missing_skills}

    items = []
    for result in raw_results:
        item = dict(result)
        course_skills_raw = [s.strip() for s in str(item.get('skills', '')).split(';') if s.strip()]
        course_skills_lower = {s.lower() for s in course_skills_raw}
        course_name_lower = str(item.get('course_name', '')).lower()

        # Identify matched skills
        matched = []
        for sk in required_skills:
            if sk.lower() in course_skills_lower or sk.lower() in course_name_lower:
                matched.append(sk)
        for sk in parsed.get('desired_skills', []):
            if (sk.lower() in course_skills_lower or sk.lower() in course_name_lower) and sk not in matched:
                matched.append(sk)

        item['matched_skills'] = matched

        # Career match score
        if career_skills_lower:
            overlap_career = sum(1 for sk in career_skills_lower if sk in course_skills_lower or sk in course_name_lower)
            item['career_match_score'] = min(overlap_career / max(len(career_skills_lower), 1), 1.0)
        else:
            item['career_match_score'] = 0.5

        # Skill gap closure score (higher if it covers missing skills)
        if missing_skills_lower:
            gap_overlap = sum(1 for sk in missing_skills_lower if sk in course_skills_lower or sk in course_name_lower)
            item['skill_score'] = min(gap_overlap / max(len(missing_skills_lower), 1), 1.0)
        elif career_skills_lower:
            item['skill_score'] = item['career_match_score']
        else:
            item['skill_score'] = 0.5

        # Difficulty alignment score
        course_diff = str(item.get('difficulty', 'Unknown')).lower()
        if effective_diff.lower() in {'beginner', 'basics', 'foundations'}:
            item['difficulty_score'] = 1.0 if 'begin' in course_diff else (0.6 if 'mixed' in course_diff else 0.3)
        elif effective_diff.lower() in {'advanced', 'expert'}:
            item['difficulty_score'] = 1.0 if 'adv' in course_diff else (0.7 if 'intermed' in course_diff else 0.2)
        elif effective_diff.lower() in {'intermediate'}:
            item['difficulty_score'] = 1.0 if 'intermed' in course_diff or 'mixed' in course_diff else 0.5
        else:
            item['difficulty_score'] = 0.8

        # Rating score normalized to [0, 1]
        raw_rating = item.get('rating')
        item['rating_score'] = (float(raw_rating) / 5.0) if raw_rating and float(raw_rating) > 0 else 0.7
        item['semantic_score'] = float(item.get('semantic_score', 0.5))

        # Grounded factual explanation
        item['explanation'] = _generate_explanation(
            item=item,
            target_career=effective_career,
            matched_skills=matched,
            missing_skills=missing_skills,
            difficulty_pref=effective_diff,
        )

        items.append(item)

    # 4. Multi-signal Hybrid Reranking
    ranked_items = hybrid_rank(items)
    final_recommendations = ranked_items[:top_k]

    # 5. Prerequisite graph for required skills
    prereqs = build_prerequisite_graph(required_skills if required_skills else parsed.get('desired_skills', []))

    # 6. Structured Learning Path
    learning_path = build_learning_path({
        'current_skills': current,
        'target_career': effective_career,
        'missing_skills': missing_skills,
        'target_skills': parsed.get('desired_skills', []),
        'recommended_courses': final_recommendations,
    })

    # 7. LLM-powered RAG answer generation (OpenRouter)
    llm_answer = generate_rag_answer(
        query=query,
        parsed_query=parsed,
        recommendations=final_recommendations,
        skill_gap=skill_gap,
        learning_path=learning_path,
    )

    return {
        'query': _json_safe(parsed),
        'skill_gap': _json_safe(skill_gap),
        'recommendations': [_json_safe(item) for item in final_recommendations],
        'prerequisites': _json_safe(prereqs),
        'learning_path': [_json_safe(step) for step in learning_path],
        'llm_answer': llm_answer,
    }
