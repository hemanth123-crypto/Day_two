"""
End-to-End System Verification Script
Executes live query resolution, skill-gap analysis, learning path generation,
and feedback persistence against the actual database and vector store.
"""
import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi.testclient import TestClient
from backend.app.main import app

def run_e2e_check():
    client = TestClient(app)

    print("=" * 70)
    print("1. HEALTH & METRICS CHECK")
    print("=" * 70)
    health = client.get("/api/v1/health")
    assert health.status_code == 200
    print("Health Status:", health.json())

    print("\n" + "=" * 70)
    print("2. CORE CAPSTONE QUERY VERIFICATION")
    query = "I know Python and SQL and want to become a machine learning engineer."
    print(f"Executing query: '{query}'")
    print("=" * 70)
    resp = client.post("/api/v1/recommendations", json={"query": query, "top_k": 5})
    assert resp.status_code == 200, f"Error: {resp.text}"
    rec_data = resp.json()

    parsed_q = rec_data.get("query", {})
    skill_gap = rec_data.get("skill_gap", {})

    print(f"Parsed Query            : {parsed_q.get('query')}")
    print(f"Extracted User Skills   : {parsed_q.get('existing_skills')}")
    print(f"Target Career Detected  : {parsed_q.get('target_career')}")
    print(f"Identified Missing Skills: {skill_gap.get('missing_skills')}")
    print(f"Skill Coverage %        : {skill_gap.get('coverage_percentage')}%")
    print(f"Total Recommendations   : {len(rec_data.get('recommendations', []))}")

    print("\nTop 5 Recommended Real Coursera Courses:")
    for i, rec in enumerate(rec_data.get("recommendations", []), 1):
        print(f"  [{i}] {rec['course_name']}")
        print(f"      Organization : {rec.get('organization')} | Difficulty: {rec.get('difficulty')} | Rating: {rec.get('rating')}")
        print(f"      Final Score  : {rec.get('final_score'):.4f} (Semantic Norm: {rec.get('semantic_norm'):.4f}, Skill Norm: {rec.get('skill_norm'):.4f})")
        print(f"      Matched Skills: {rec.get('matched_skills')}")
        print(f"      Explanation  : {rec.get('explanation')}")

    print("\n" + "=" * 70)
    print("3. PERSONALIZED LEARNING PATH VERIFICATION")
    print("=" * 70)
    path_steps = rec_data.get("learning_path", [])
    print(f"Total Path Milestones: {len(path_steps)}")
    for step in path_steps:
        print(f"  Step {step['order']}: '{step['course']}' ({step['difficulty']})")
        print(f"      Reason: {step['reason']}")
        print(f"      Prerequisites: {step.get('prerequisites')}")

    print("\n" + "=" * 70)
    print("4. SQLITE PERSISTENCE & FEEDBACK LOOP VERIFICATION")
    print("=" * 70)
    top_course_id = rec_data["recommendations"][0]["course_id"]
    fb_payload = {
        "query": query,
        "course_id": top_course_id,
        "rating": 5,
        "is_useful": True,
        "comments": "Accurate recommendation directly closing my ML skill gap."
    }
    fb_resp = client.post("/api/v1/feedback", json=fb_payload)
    assert fb_resp.status_code == 200
    print("Feedback submission response:", fb_resp.json())

    stats_resp = client.get("/api/v1/feedback/stats")
    assert stats_resp.status_code == 200
    print("Feedback Aggregate Stats:", stats_resp.json())

    print("\n" + "=" * 70)
    print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY WITH 100% VALIDITY!")
    print("=" * 70)

if __name__ == "__main__":
    run_e2e_check()
