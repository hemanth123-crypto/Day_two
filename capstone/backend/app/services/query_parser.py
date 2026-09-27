from __future__ import annotations
import re
from typing import Any, Dict, List, Optional, Set

from backend.app.knowledge_base.career_mapping import get_career_target
from backend.app.knowledge_base.skill_taxonomy import canonicalize_skill_name, SKILL_TAXONOMY, SKILL_ALIASES

# Skill phrase list sorted by length descending so multi-word skills match first
_SORTED_SKILL_PHRASES = sorted(SKILL_ALIASES.keys(), key=lambda x: len(x), reverse=True)


def extract_skills_from_text(text: str) -> List[str]:
    """Find all matching canonical skills mentioned anywhere in the given text snippet."""
    if not text:
        return []
    lowered = text.lower()
    found: List[str] = []
    
    # Use word boundary or punctuation checks
    for phrase in _SORTED_SKILL_PHRASES:
        pattern = r'(?:\b|_)' + re.escape(phrase) + r'(?:\b|_)'
        if re.search(pattern, lowered):
            canonical = canonicalize_skill_name(phrase)
            if canonical and canonical not in found:
                found.append(canonical)
                # Remove matched phrase to prevent double matching substring skills
                lowered = re.sub(pattern, ' ', lowered)
    return found


def extract_difficulty(text: str) -> str:
    """Infer preferred difficulty level from natural language query."""
    lowered = text.lower()
    if any(k in lowered for k in ['from the basics', 'from scratch', 'beginner', 'basics', 'introduction', 'introductory', 'start with', 'foundations']):
        return 'Beginner'
    if any(k in lowered for k in ['advanced', 'expert', 'mastery', 'deep dive', 'cutting-edge']):
        return 'Advanced'
    if any(k in lowered for k in ['intermediate', 'mid-level', 'beyond basics', 'next step']):
        return 'Intermediate'
    return 'Any'


def extract_domain(text: str) -> str:
    """Infer domain/field from query text."""
    lowered = text.lower()
    if any(k in lowered for k in ['data science', 'data analytics', 'data analyst', 'statistics']):
        return 'Data Science'
    if any(k in lowered for k in ['machine learning', 'deep learning', 'artificial intelligence', 'ai', 'predictive']):
        return 'Artificial Intelligence'
    if any(k in lowered for k in ['cloud', 'aws', 'azure', 'gcp', 'devops', 'kubernetes']):
        return 'Cloud Computing'
    if any(k in lowered for k in ['software', 'developer', 'web', 'frontend', 'backend', 'full stack', 'programming']):
        return 'Software Engineering'
    return 'General'


def parse_user_query(text: str) -> Dict[str, Any]:
    """
    Intelligent natural language query parser for student learning intents.
    Differentiates:
    - Existing skills (what the user already knows)
    - Desired skills / Target (what the user wants to learn)
    - Weak skills (skills explicitly noted as weak or missing)
    - Target career or goal
    - Preferred difficulty and domain
    """
    if not text or not str(text).strip():
        raise ValueError('Query cannot be empty.')

    raw_text = str(text).strip()
    lowered = raw_text.lower()

    # Detect target career
    target_career = get_career_target(raw_text)

    # Clause segmentation for existing skills vs target goals
    existing_skills: List[str] = []
    desired_skills: List[str] = []
    weak_skills: List[str] = []

    # Patterns for existing skills: "I know X", "my skills are X", "familiar with X", "experience with X"
    know_patterns = [
        r'(?:i know|i have experience with|i am familiar with|familiar with|already know|proficient in|background in|worked with|i understand)\s+([^.,;!?]+?)(?=\s+(?:and|but)?\s*(?:want|wish|need|looking|aim|weak|interested|to move|next)|[.,;!?]|$)',
        r'(?:my skills are|current skills:?|existing skills:?)\s*([^.,;!?]+?)(?=\s+(?:and|but)?\s*(?:want|wish|need|looking|aim|weak)|[.,;!?]|$)',
    ]
    for pattern in know_patterns:
        match = re.search(pattern, lowered)
        if match:
            clause = match.group(1)
            skills = extract_skills_from_text(clause)
            for s in skills:
                if s not in existing_skills:
                    existing_skills.append(s)

    # Patterns for weak areas: "weak in X", "struggling with X", "need help with X"
    weak_patterns = [
        r'(?:weak in|not good at|struggling with|lack|rusty in|need to learn)\s+([^.,;!?]+?)(?=[.,;!?]|$)',
    ]
    for pattern in weak_patterns:
        match = re.search(pattern, lowered)
        if match:
            clause = match.group(1)
            skills = extract_skills_from_text(clause)
            for s in skills:
                if s not in weak_skills:
                    weak_skills.append(s)
                if s not in desired_skills:
                    desired_skills.append(s)

    # Patterns for target / desired goals: "want to learn X", "move into X", "interested in X", "courses for X"
    want_patterns = [
        r'(?:want to learn|looking to learn|wish to learn|aiming to learn|interested in|move into|transition to|become a|become an|prepare for|courses for|learn)\s+([^.,;!?]+?)(?=[.,;!?]|$)',
    ]
    for pattern in want_patterns:
        match = re.search(pattern, lowered)
        if match:
            clause = match.group(1)
            skills = extract_skills_from_text(clause)
            for s in skills:
                if s not in desired_skills:
                    desired_skills.append(s)

    # If no existing skills were caught by explicit clauses, check if the whole text has skills,
    # but only treat them as existing if there is an explicit target statement.
    if not existing_skills:
        # If there's an explicit "want to learn" or "become", any skills BEFORE that might be known
        split_target = re.split(r'\b(?:want to|wish to|looking to|to move into|to become)\b', lowered)
        if len(split_target) > 1:
            pre_clause = split_target[0]
            pre_skills = extract_skills_from_text(pre_clause)
            for s in pre_skills:
                if s not in existing_skills and s not in desired_skills:
                    existing_skills.append(s)

    # If desired skills is still empty, extract all skills from the query that are NOT in existing_skills
    all_query_skills = extract_skills_from_text(raw_text)
    for s in all_query_skills:
        if s not in existing_skills and s not in desired_skills:
            desired_skills.append(s)

    # Clean existing skills to make sure none of them were marked as weak
    for w in weak_skills:
        if w in existing_skills:
            existing_skills.remove(w)

    difficulty = extract_difficulty(raw_text)
    domain = extract_domain(raw_text)

    # If target career was not found directly, infer from desired skills or domain
    if not target_career:
        if 'Machine Learning' in desired_skills or 'Deep Learning' in desired_skills:
            target_career = 'Machine Learning Engineer'
        elif 'Cloud Computing' in desired_skills or 'AWS' in desired_skills or 'Azure' in desired_skills:
            target_career = 'Cloud Engineer'
        elif 'Data Analysis' in desired_skills or 'Power BI' in desired_skills or 'Tableau' in desired_skills:
            target_career = 'Data Analyst'
        elif 'Data Science' in raw_text.title() or ('Python' in desired_skills and 'Statistics' in desired_skills):
            target_career = 'Data Scientist'

    return {
        'query': raw_text,
        'existing_skills': existing_skills,
        'target_career': target_career,
        'desired_skills': desired_skills,
        'weak_skills': weak_skills,
        'difficulty': difficulty,
        'domain': domain,
    }
