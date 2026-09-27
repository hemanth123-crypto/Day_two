import pandas as pd

from backend.app.services.skill_service import normalize_skill
from backend.scripts.preprocess_data import normalize_difficulty, normalize_rating


def test_normalize_skill_variants():
    assert normalize_skill('python programming') == 'Python'
    assert normalize_skill('machine-learning') == 'Machine Learning'
    assert normalize_skill('data analytics') == 'Data Analysis'


def test_normalize_difficulty():
    assert normalize_difficulty('beginner') == 'Beginner'
    assert normalize_difficulty('Advanced') == 'Advanced'
    assert normalize_difficulty('mixed') == 'Intermediate'


def test_normalize_rating():
    assert normalize_rating('4.7') == 4.7
    assert normalize_rating('N/A') is None
