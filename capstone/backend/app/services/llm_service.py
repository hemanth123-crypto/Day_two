from __future__ import annotations
import json
import logging
from typing import Any, Dict, List, Optional

import httpx

from backend.app.config import OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_BASE_URL, APP_NAME

logger = logging.getLogger(__name__)


def is_llm_available() -> bool:
    """Check whether OpenRouter LLM is configured with a valid API key."""
    return bool(OPENROUTER_API_KEY and OPENROUTER_API_KEY.strip())


def _build_rag_prompt(
    query: str,
    parsed_query: Dict[str, Any],
    recommendations: List[Dict[str, Any]],
    skill_gap: Dict[str, Any],
    learning_path: List[Dict[str, Any]],
) -> str:
    """
    Construct a RAG prompt that grounds the LLM response in retrieved course data.
    The prompt includes the student's query, parsed intent, skill gap analysis,
    recommended courses with scores, and the learning path — all factual data
    from the retrieval pipeline.
    """
    # Format recommended courses as context
    course_context_lines = []
    for i, course in enumerate(recommendations[:10], 1):
        name = course.get('course_name', 'Unknown')
        org = course.get('organization', '')
        diff = course.get('difficulty', '')
        rating = course.get('rating', 0)
        skills = course.get('skills', '')
        score = course.get('final_score', 0)
        explanation = course.get('explanation', '')
        matched = ', '.join(course.get('matched_skills', []))
        course_context_lines.append(
            f"{i}. **{name}** by {org}\n"
            f"   - Difficulty: {diff} | Rating: {rating}/5.0 | Relevance Score: {score:.2f}\n"
            f"   - Skills Covered: {skills}\n"
            f"   - Matched Skills: {matched}\n"
            f"   - System Note: {explanation}"
        )
    courses_block = '\n'.join(course_context_lines)

    # Format skill gap
    existing = ', '.join(skill_gap.get('existing_skills', [])) or 'None specified'
    missing = ', '.join(skill_gap.get('missing_skills', [])) or 'None'
    required = ', '.join(skill_gap.get('required_skills', [])) or 'General'
    coverage = skill_gap.get('coverage_percentage', 0)

    # Format learning path
    path_lines = []
    for step in learning_path[:8]:
        order = step.get('order', '?')
        course = step.get('course', '')
        step_skills = ', '.join(step.get('skills', []))
        reason = step.get('reason', '')
        path_lines.append(f"  Step {order}: {course} — Skills: {step_skills} — {reason}")
    path_block = '\n'.join(path_lines) if path_lines else 'No structured path generated.'

    # Parsed intent
    target_career = parsed_query.get('target_career', 'General')
    desired = ', '.join(parsed_query.get('desired_skills', [])) or 'Not specified'
    difficulty = parsed_query.get('difficulty', 'Any')

    prompt = f"""You are a helpful, expert university course advisor for the "University Course Finder" system.
A student has asked the following question, and our retrieval system has found relevant courses from a catalog of 884 real Coursera courses.

Your job is to synthesize the retrieved data into a clear, personalized, and actionable answer for the student.

## RULES:
1. ONLY recommend courses that appear in the retrieved data below. Do NOT invent or hallucinate course names.
2. Ground every recommendation in the factual data provided (ratings, skills, difficulty, organization).
3. Be concise but comprehensive. Use a warm, encouraging, professional tone.
4. Structure your answer with: a brief personalized summary, key course recommendations with reasons, and a suggested learning sequence.
5. Mention the student's skill gaps and how the recommended courses address them.
6. If a learning path is provided, reference it naturally.

---

## STUDENT QUERY:
"{query}"

## PARSED INTENT:
- Target Career: {target_career}
- Desired Skills: {desired}
- Preferred Difficulty: {difficulty}
- Existing Skills: {existing}

## SKILL GAP ANALYSIS:
- Required Skills for {target_career}: {required}
- Missing Skills: {missing}
- Current Coverage: {coverage:.0f}%

## RETRIEVED COURSES (ranked by hybrid relevance score):
{courses_block}

## SUGGESTED LEARNING PATH:
{path_block}

---

Now provide a clear, grounded, personalized response to the student. Do not use markdown headers larger than ###. Keep it under 400 words."""

    return prompt


def generate_rag_answer(
    query: str,
    parsed_query: Dict[str, Any],
    recommendations: List[Dict[str, Any]],
    skill_gap: Dict[str, Any],
    learning_path: List[Dict[str, Any]],
) -> Optional[str]:
    """
    Call OpenRouter API to generate a RAG-grounded answer using retrieved course data.
    Returns the LLM response text, or None if the LLM is unavailable or fails.
    """
    if not is_llm_available():
        logger.info("OpenRouter API key not configured. Skipping LLM answer generation.")
        return None

    prompt = _build_rag_prompt(query, parsed_query, recommendations, skill_gap, learning_path)

    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost:5173',
        'X-Title': APP_NAME,
    }

    payload = {
        'model': OPENROUTER_MODEL,
        'messages': [
            {
                'role': 'system',
                'content': (
                    'You are an expert educational course advisor. '
                    'You provide personalized, data-grounded course recommendations. '
                    'You never invent course names — only reference courses provided in the context.'
                ),
            },
            {
                'role': 'user',
                'content': prompt,
            },
        ],
        'temperature': 0.4,
        'max_tokens': 1200,
    }

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f'{OPENROUTER_BASE_URL}/chat/completions',
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

            # Extract the assistant message content
            choices = data.get('choices', [])
            if choices and choices[0].get('message', {}).get('content'):
                answer = choices[0]['message']['content'].strip()
                logger.info(f"LLM answer generated successfully ({len(answer)} chars, model={OPENROUTER_MODEL})")
                return answer

            logger.warning(f"OpenRouter returned empty response: {data}")
            return None

    except httpx.HTTPStatusError as exc:
        logger.error(f"OpenRouter API error {exc.response.status_code}: {exc.response.text}")
        return None
    except httpx.TimeoutException:
        logger.error("OpenRouter API request timed out after 30s.")
        return None
    except Exception as exc:
        logger.error(f"Unexpected error calling OpenRouter API: {exc}")
        return None
