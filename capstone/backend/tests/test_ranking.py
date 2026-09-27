from backend.app.services.ranking_service import normalize_scores, hybrid_rank


def test_normalize_scores():
    values = [1.0, 3.0, 5.0]
    normalized = normalize_scores(values)
    assert isinstance(normalized, list)
    assert normalized[0] == 0.0
    assert normalized[-1] == 1.0


def test_hybrid_rank_uses_weights():
    items = [
        {'semantic_score': 0.8, 'skill_score': 0.7, 'difficulty_score': 0.6, 'rating_score': 0.9},
        {'semantic_score': 0.2, 'skill_score': 0.3, 'difficulty_score': 0.1, 'rating_score': 0.2},
    ]
    scored = hybrid_rank(items)
    assert scored[0]['final_score'] >= scored[1]['final_score']
