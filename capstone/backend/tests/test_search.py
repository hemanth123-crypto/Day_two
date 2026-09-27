from backend.app.services.query_parser import parse_user_query
from backend.app.services.search_service import search_courses


def test_search_empty_query_raises():
    try:
        search_courses('', top_k=5)
        assert False, 'Expected validation error for empty query'
    except ValueError:
        pass


def test_search_returns_list_for_known_term():
    results = search_courses('python machine learning', top_k=5)
    assert isinstance(results, list)


def test_software_engineering_query_maps_to_engineer_career():
    parsed = parse_user_query('software enginner')
    assert parsed['target_career'] == 'Software Engineer'
