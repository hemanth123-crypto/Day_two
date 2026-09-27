from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_list_courses_endpoint():
    response = client.get('/api/v1/courses?page=1&page_size=5')
    assert response.status_code == 200
    data = response.json()
    assert 'courses' in data
    assert 'total' in data
    assert len(data['courses']) <= 5


def test_get_single_course():
    response = client.get('/api/v1/courses/course_0000')
    assert response.status_code == 200
    data = response.json()
    assert data['course_id'] == 'course_0000'
    assert 'course_name' in data


def test_get_course_not_found():
    response = client.get('/api/v1/courses/course_nonexistent_99999')
    assert response.status_code == 404


def test_search_endpoint():
    response = client.post('/api/v1/courses/search', json={'query': 'Python for data science', 'top_k': 3})
    assert response.status_code == 200
    assert 'courses' in response.json()


def test_recommendation_endpoint():
    response = client.post('/api/v1/recommendations', json={
        'query': 'I know Python and SQL and want to become a machine learning engineer.',
        'top_k': 3
    })
    assert response.status_code == 200
    data = response.json()
    assert 'recommendations' in data
    assert 'skill_gap' in data
    assert 'learning_path' in data
    assert len(data['recommendations']) > 0
    assert len(data['learning_path']) > 0


def test_skills_analyze_endpoint():
    response = client.post('/api/v1/skills/analyze', json={
        'current_skills': ['Python', 'SQL'],
        'target_career': 'Data Scientist'
    })
    assert response.status_code == 200
    data = response.json()
    assert 'missing_skills' in data
    assert 'coverage_percentage' in data
    assert 'Python' in data['existing_skills']


def test_skills_taxonomy_and_careers_endpoints():
    r1 = client.get('/api/v1/skills/taxonomy')
    assert r1.status_code == 200
    assert len(r1.json()['skills']) > 0

    r2 = client.get('/api/v1/skills/careers')
    assert r2.status_code == 200
    assert len(r2.json()['careers']) > 0


def test_learning_path_endpoint():
    response = client.post('/api/v1/learning-path', json={
        'current_skills': ['Python'],
        'target_career': 'Machine Learning Engineer',
        'missing_skills': ['Statistics', 'Machine Learning', 'Deep Learning'],
    })
    assert response.status_code == 200
    data = response.json()
    assert data['total_steps'] > 0
    assert len(data['path']) > 0
    assert data['path'][0]['order'] == 1


def test_feedback_submit_and_stats():
    # Submit test feedback
    response = client.post('/api/v1/feedback', json={
        'course_id': 'course_0000',
        'rating': 5,
        'useful': True,
        'comment': 'High quality course recommendation!'
    })
    assert response.status_code == 200
    data = response.json()
    assert 'feedback_id' in data

    # Retrieve feedback stats
    stats_resp = client.get('/api/v1/feedback/stats')
    assert stats_resp.status_code == 200
    stats = stats_resp.json()
    assert stats['total_feedback'] >= 1
    assert stats['average_rating'] > 0


def test_recommendation_evaluate_endpoint():
    response = client.post('/api/v1/recommendations/evaluate', json={
        'query': 'I know Python and want to learn machine learning.',
        'top_k': 3,
    })
    assert response.status_code == 200
    data = response.json()
    assert 'query' in data
    assert 'evaluations' in data
    assert 'evaluation_methodology' in data
    assert len(data['evaluations']) > 0
    first = data['evaluations'][0]
    assert 'factors' in first
    assert 'prerequisite_readiness' in first
    assert 'detailed_justification' in first


def test_benchmark_endpoint():
    response = client.get('/api/v1/recommendations/benchmark')
    assert response.status_code == 200
    data = response.json()
    assert 'precision_at_3' in data
    assert 'ndcg_at_3' in data
    assert 'learning_path_validity_pct' in data
    assert 'queries' in data
    assert len(data['queries']) == 10
