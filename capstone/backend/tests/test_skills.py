from backend.app.services.skill_service import get_skill_gap, normalize_skill


def test_existing_skill_detection():
    current = ['Python', 'SQL']
    target = 'Machine Learning Engineer'
    gap = get_skill_gap(current, target)
    assert 'Python' not in gap['missing_skills']
    assert 'Machine Learning' in gap['missing_skills']


def test_normalize_skill_handles_aliases():
    assert normalize_skill('numpy') == 'NumPy'
    assert normalize_skill('ml') == 'Machine Learning'
