from __future__ import annotations
from fastapi import APIRouter, HTTPException

from backend.app.knowledge_base.career_mapping import CAREER_SKILLS
from backend.app.knowledge_base.skill_taxonomy import SKILL_TAXONOMY
from backend.app.schemas.skill import SkillAnalysisRequest
from backend.app.services.skill_service import get_skill_gap

router = APIRouter(prefix='/skills', tags=['skills'])


@router.get('/taxonomy')
def list_skill_taxonomy():
    """Return all normalized skills tracked in the centralized skill taxonomy."""
    return {'count': len(SKILL_TAXONOMY), 'skills': SKILL_TAXONOMY}


@router.get('/careers')
def list_career_profiles():
    """Return tracked career roles and their standard industry skill requirements."""
    return {
        'count': len(CAREER_SKILLS),
        'careers': [
            {'career': career, 'required_skills': skills}
            for career, skills in CAREER_SKILLS.items()
        ]
    }


@router.post('/analyze')
def analyze_skills(request: SkillAnalysisRequest):
    """
    Skill gap analysis endpoint:
    - Compares student's current skills against target career competencies
    - Identifies existing competencies and missing skill gaps
    - Computes skill coverage percentage
    - Recommends top-rated courses to close each missing skill gap
    """
    try:
        result = get_skill_gap(
            current_skills=request.current_skills,
            target_career=request.target_career,
            target_skills=request.target_skills,
            include_courses_for_missing=True,
        )
        return result
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
