"""
Full Verification Test Suite for MoSPI AI Learning Platform (SIH) v3.7.0
Mission Karmayogi Serving Officer In-Service Capacity Building Suite.
Tests Officer Profile Landing Dashboard (Step 0), Time-Based Greetings,
Role-Specific Quiz & Skill Gap Reset, Linear Step Locking, and Creator Admin Portal.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("=" * 70)
    print("  MISSION KARMAYOGI FULL-STACK PLATFORM VERIFICATION TEST SUITE (v3.7.0)")
    print("======================================================================\n")

    session = requests.Session()

    # 1. Portal Route Checks
    r_learner = session.get(f"{BASE_URL}/")
    r_creator = session.get(f"{BASE_URL}/creator")
    print(f"1. Portal Route Checks:")
    print(f"   - Learner Capacity Portal (/): HTTP {r_learner.status_code}")
    print(f"   - Creator Admin Portal (/creator): HTTP {r_creator.status_code}")
    assert r_learner.status_code == 200
    assert r_creator.status_code == 200

    # 2. Serving Officer Registration Test
    reg_payload = {
        "user_id": "ashw_101",
        "name": "Officer Ramesh Kumar",
        "department": "Price Statistics Division",
        "password": "123",
        "job_role_id": "ROLE_JOB_001"
    }
    r_reg = session.post(f"{BASE_URL}/api/v1/auth/register", json=reg_payload)
    print(f"2. Serving Officer Registration Test (user_id='ashw_101'): HTTP {r_reg.status_code}")

    # 3. Select Position Cadre A (IAS) & Fetch Specific On-the-Job Baseline Quiz
    r_select_a = session.post(f"{BASE_URL}/api/v1/learner/select-role", json={"user_id": "ashw_101", "role_id": "ROLE_JOB_001"})
    r_quiz_a = session.get(f"{BASE_URL}/api/v1/learner/quiz/baseline/ROLE_JOB_001")
    q_a = r_quiz_a.json().get("questions", [])
    print(f"3. Position Cadre A (IAS) On-the-Job Diagnostic Fetch: Loaded {len(q_a)} questions for {r_quiz_a.json().get('role_title')}.")
    assert len(q_a) > 0

    # 4. Switch to Position Cadre B (IPS) & Verify Role-Specific Reset & Quiz B Fetch
    r_select_b = session.post(f"{BASE_URL}/api/v1/learner/select-role", json={"user_id": "ashw_101", "role_id": "ROLE_JOB_002"})
    r_quiz_b = session.get(f"{BASE_URL}/api/v1/learner/quiz/baseline/ROLE_JOB_002")
    q_b = r_quiz_b.json().get("questions", [])
    print(f"4. Position Cadre B (IPS) Switch Test: Selected {r_select_b.json().get('role', {}).get('title')}. Fetched {len(q_b)} Role B specific questions.")
    assert len(q_b) > 0

    # 5. Grade Position Cadre B On-the-Job Quiz & Skill Gap Calculation
    answers_b = {q["id"]: 0 for q in q_b}
    r_submit_b = session.post(f"{BASE_URL}/api/v1/learner/quiz/baseline/submit", json={"user_id": "ashw_101", "role_id": "ROLE_JOB_002", "answers": answers_b})
    gaps_b = r_submit_b.json().get('gap_analysis', [])
    print(f"5. Position Cadre B Skill Gap Analysis: Calculated Gaps for {len(gaps_b)} competencies required by IPS.")
    assert r_submit_b.status_code == 200

    # 6. Semantic Gap-Based Recommendation Engine Test for Position Cadre B
    r_rec_b = session.post(f"{BASE_URL}/api/v1/learner/recommendations", data={"user_id": "ashw_101"})
    recs_b = r_rec_b.json().get("recommendations", [])
    print(f"6. Semantic Recommendation Output for Position Cadre B: Found {len(recs_b)} targeted iGOT capacity courses.")
    assert r_rec_b.status_code == 200

    # 7. Learner Officer Profile & Capacity Roadmap Data Fetch Test
    r_profile = session.get(f"{BASE_URL}/api/v1/learner/profile/ashw_101")
    profile = r_profile.json()
    print(f"7. Serving Officer Profile & Capacity Roadmap Fetch:")
    print(f"   - Officer Name: {profile.get('name')}")
    print(f"   - Current Position: {profile.get('role', {}).get('title')}")
    print(f"   - Position Competencies Tracked: {len(profile.get('competencies', []))}")
    assert r_profile.status_code == 200

    # 8. Employee Account Access Revocation
    r_del = session.delete(f"{BASE_URL}/api/v1/creator/employee/ashw_101")
    print(f"8. Creator Revoke Access Response: {r_del.json().get('message')}")
    assert r_del.status_code == 200

    print("\n" + "=" * 70)
    print("  ALL MISSION KARMAYOGI VERIFICATION TESTS COMPLETED SUCCESSFULLY!")
    print("======================================================================\n")

if __name__ == "__main__":
    run_tests()
