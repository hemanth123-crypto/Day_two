from __future__ import annotations
import math
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from backend.app.config import TOP_K
from backend.app.schemas.course import CourseListResponse, CourseResponse, CourseSearchRequest
from backend.app.services.search_service import _load_processed_courses, _json_safe, search_courses

router = APIRouter(prefix='/courses', tags=['courses'])


@router.get('', response_model=CourseListResponse)
def list_courses(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
    difficulty: Optional[str] = Query(default=None, description="Filter by difficulty"),
    search: Optional[str] = Query(default=None, description="Filter by keyword in course name or skills"),
    organization: Optional[str] = Query(default=None, description="Filter by institution / organization"),
):
    """
    List courses with pagination and optional filtering by difficulty, organization, or search term.
    """
    try:
        df = _load_processed_courses()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    filtered_df = df
    if difficulty and difficulty.lower() not in {'all', 'any'}:
        filtered_df = filtered_df[filtered_df['difficulty'].str.lower() == difficulty.lower()]
    if organization:
        filtered_df = filtered_df[filtered_df['organization'].str.contains(organization, case=False, na=False)]
    if search:
        search_lower = search.lower()
        mask = (
            filtered_df['course_name'].str.contains(search_lower, case=False, na=False)
            | filtered_df['skills'].str.contains(search_lower, case=False, na=False)
            | filtered_df['description'].str.contains(search_lower, case=False, na=False)
        )
        filtered_df = filtered_df[mask]

    total = len(filtered_df)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    sliced = filtered_df.iloc[start_idx:end_idx]
    records = [_json_safe(r) for r in sliced.to_dict(orient='records')]

    return CourseListResponse(
        count=len(records),
        total=total,
        page=page,
        page_size=page_size,
        courses=records,
    )


@router.get('/{course_id}', response_model=CourseResponse)
def get_course(course_id: str):
    """
    Retrieve full details for a specific course by course_id.
    """
    try:
        df = _load_processed_courses()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    match = df[df['course_id'].astype(str) == str(course_id)]
    if match.empty:
        raise HTTPException(status_code=404, detail=f"Course with ID '{course_id}' not found.")
    
    course_data = _json_safe(match.iloc[0].to_dict())
    return CourseResponse(**course_data)


@router.post('/search')
def search_courses_endpoint(request: CourseSearchRequest):
    """
    Perform semantic vector search using FAISS with multi-parameter filtering.
    """
    try:
        results = search_courses(
            query=request.query,
            top_k=request.top_k,
            difficulty=request.difficulty,
            min_rating=request.min_rating,
        )
        return {
            'query': request.query,
            'count': len(results),
            'courses': results,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(exc)}")
