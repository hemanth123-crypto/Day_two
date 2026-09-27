from backend.app.services.prerequisite_service import build_prerequisite_graph, detect_cycle, order_skills


def test_graph_cycle_detection():
    graph = {'Python': ['Statistics'], 'Statistics': ['Python']}
    assert detect_cycle(graph) is True


def test_dependency_ordering():
    graph = {'Python': ['Statistics'], 'Statistics': ['Machine Learning'], 'Machine Learning': []}
    ordered = order_skills(graph)
    assert ordered[0] == 'Python'
    assert ordered[-1] == 'Machine Learning'
