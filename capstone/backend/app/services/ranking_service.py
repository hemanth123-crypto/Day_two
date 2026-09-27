from __future__ import annotations
from typing import Any, Dict, List, Optional

from backend.app.config import (
    SEMANTIC_WEIGHT,
    SKILL_WEIGHT,
    DIFFICULTY_WEIGHT,
    RATING_WEIGHT,
)


def normalize_scores(values: List[float]) -> List[float]:
    """
    Min-max normalize a list of float scores to [0.0, 1.0].
    Handles single-element lists, constant values, and edge cases gracefully.
    """
    if not values:
        return []
    minimum = min(values)
    maximum = max(values)
    if maximum == minimum:
        # If all values are identical and positive, assign 1.0; if zero/negative, 0.0
        val = 1.0 if maximum > 0 else 0.0
        return [val for _ in values]
    return [round((value - minimum) / (maximum - minimum), 4) for value in values]


def hybrid_rank(
    items: List[Dict[str, Any]],
    semantic_weight: float = SEMANTIC_WEIGHT,
    skill_weight: float = SKILL_WEIGHT,
    difficulty_weight: float = DIFFICULTY_WEIGHT,
    rating_weight: float = RATING_WEIGHT,
    career_weight: float = 0.10,
) -> List[Dict[str, Any]]:
    """
    Reranks candidate courses using multi-signal hybrid scoring:
    - Semantic similarity score from FAISS
    - Skill overlap score with user's target / missing skills
    - Difficulty alignment score
    - Course rating score
    - Career match keyword score

    Weights are configurable and each component is normalized to [0, 1] before combination.
    """
    if not items:
        return []

    # Normalize total weights to sum to 1.0
    total_w = semantic_weight + skill_weight + difficulty_weight + rating_weight + career_weight
    if total_w <= 0:
        total_w = 1.0
    w_sem = semantic_weight / total_w
    w_sk = skill_weight / total_w
    w_diff = difficulty_weight / total_w
    w_rat = rating_weight / total_w
    w_car = career_weight / total_w

    sem = [float(item.get('semantic_score', 0.0) or 0.0) for item in items]
    skill = [float(item.get('skill_score', 0.0) or 0.0) for item in items]
    diff = [float(item.get('difficulty_score', 0.0) or 0.0) for item in items]
    rating = [float(item.get('rating_score', 0.0) or 0.0) for item in items]
    career = [float(item.get('career_match_score', 0.0) or 0.0) for item in items]

    s_norm = normalize_scores(sem)
    sk_norm = normalize_scores(skill)
    d_norm = normalize_scores(diff)
    r_norm = normalize_scores(rating)
    c_norm = normalize_scores(career)

    for idx, item in enumerate(items):
        item['semantic_norm'] = s_norm[idx]
        item['skill_norm'] = sk_norm[idx]
        item['difficulty_norm'] = d_norm[idx]
        item['rating_norm'] = r_norm[idx]
        item['career_norm'] = c_norm[idx]

        final = (
            w_sem * s_norm[idx]
            + w_sk * sk_norm[idx]
            + w_diff * d_norm[idx]
            + w_rat * r_norm[idx]
            + w_car * c_norm[idx]
        )
        item['final_score'] = round(final, 4)

    return sorted(items, key=lambda x: x['final_score'], reverse=True)
