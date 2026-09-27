from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query

from backend.app.database import SessionLocal
from backend.app.models.feedback import Feedback
from backend.app.schemas.feedback import FeedbackCreate, FeedbackResponse

router = APIRouter(prefix='/feedback', tags=['feedback'])


@router.post('', response_model=FeedbackResponse)
def submit_feedback(request: FeedbackCreate):
    """
    Store student feedback for courses or recommendations in SQLite.
    Collects rating (1-5 stars), usefulness flag, and optional comments.
    """
    db = SessionLocal()
    try:
        feedback = Feedback(
            course_id=request.course_id,
            rating=request.rating,
            useful=request.useful,
            comment=request.comment or '',
            created_at=datetime.utcnow()
        )
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        return FeedbackResponse(
            message='Feedback recorded successfully. Thank you for helping improve recommendations!',
            feedback_id=feedback.id,
            course_id=feedback.course_id,
            rating=feedback.rating,
            useful=feedback.useful,
            comment=feedback.comment or '',
            created_at=feedback.created_at,
        )
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to record feedback: {str(exc)}")
    finally:
        db.close()


@router.get('/stats')
def get_feedback_statistics():
    """
    Retrieve aggregated feedback metrics for evaluation:
    - Total submissions
    - Average rating
    - Positive usefulness percentage
    - Breakdown of ratings
    """
    db = SessionLocal()
    try:
        all_feedback = db.query(Feedback).all()
        total = len(all_feedback)
        if total == 0:
            return {
                'total_feedback': 0,
                'average_rating': 0.0,
                'usefulness_rate': 0.0,
                'rating_distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                'recent_feedback': [],
            }

        avg_rating = round(sum(f.rating for f in all_feedback) / total, 2)
        useful_count = sum(1 for f in all_feedback if f.useful)
        usefulness_rate = round((useful_count / total) * 100, 1)

        rating_dist = {i: 0 for i in range(1, 6)}
        for f in all_feedback:
            if f.rating in rating_dist:
                rating_dist[f.rating] += 1

        recent = [
            {
                'id': f.id,
                'course_id': f.course_id,
                'rating': f.rating,
                'useful': f.useful,
                'comment': f.comment,
                'created_at': f.created_at.isoformat() if f.created_at else None,
            }
            for f in sorted(all_feedback, key=lambda x: x.created_at or datetime.min, reverse=True)[:10]
        ]

        return {
            'total_feedback': total,
            'average_rating': avg_rating,
            'usefulness_rate': usefulness_rate,
            'rating_distribution': rating_dist,
            'recent_feedback': recent,
        }
    finally:
        db.close()
