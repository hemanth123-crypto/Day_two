from backend.app.services.learning_path_service import build_learning_path


def test_build_learning_path_basic():
    personal = {
        'current_skills': ['Python'],
        'target_career': 'Machine Learning Engineer',
        'target_skills': ['Machine Learning'],
        'missing_skills': ['Statistics', 'Machine Learning'],
        'prerequisites': {'Machine Learning': ['Statistics'], 'Statistics': ['Python']}
    }
    path = build_learning_path(personal)
    assert path
    assert path[0]['order'] == 1
    assert path[-1]['course']
