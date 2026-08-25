"""
Full Verification Test Suite for MoSPI AI Learning Platform (SIH)
Tests Creator Portal, Learner Portal, User Auth & Regex Validation,
Duplicate Officer Rejection, Employee Account Deletion, Baseline & Intermediate Quizzes,
RAG Quiz Engine, and iGOT Karmayogi Course Recommendations.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("=" * 70)
    print("  SIH FULL-STACK PLATFORM VERIFICATION TEST SUITE (v3.1.0)")
    print("======================================================================\n")

    session = requests.Session()

    # 1. Portal Route Checks
    r_learner = session.get(f"{BASE_URL}/")
    r_creator = session.get(f"{BASE_URL}/creator")
    print(f"1. Portal Route Checks:")
    print(f"   - Learner Portal (/): HTTP {r_learner.status_code}")
    print(f"   - Creator Portal (/creator): HTTP {r_creator.status_code}")
    assert r_learner.status_code == 200
    assert r_creator.status_code == 200

    # 2. User ID Format Validation Test (Invalid Format)
    bad_reg_payload = {
        "user_id": "bad",
        "name": "Test Officer",
        "department": "Price Division",
        "password": "123"
    }
    r_bad = session.post(f"{BASE_URL}/api/v1/auth/register", json=bad_reg_payload)
    print(f"\n2. Invalid User ID Regex Test (user_id='bad'): HTTP {r_bad.status_code}")
    assert r_bad.status_code == 400

    # 3. Valid User Registration Test
    valid_reg_payload = {
        "user_id": "ashw_101",
        "name": "Officer Ramesh Kumar",
        "department": "Price Statistics Division",
        "password": "123"
    }
    r_reg = session.post(f"{BASE_URL}/api/v1/auth/register", json=valid_reg_payload)
    print(f"3. Valid Registration Test (user_id='ashw_101'): HTTP {r_reg.status_code}")

    # 4. Duplicate Officer Name & Dept Registration Error Test
    r_dup = session.post(f"{BASE_URL}/api/v1/auth/register", json=valid_reg_payload)
    print(f"4. Duplicate Officer Error Test: HTTP {r_dup.status_code} - {r_dup.json().get('detail')}")
    assert r_dup.status_code == 400

    # 5. Login Test
    login_payload = {"user_id": "ashw_101", "password": "123"}
    r_login = session.post(f"{BASE_URL}/api/v1/auth/login", json=login_payload)
    print(f"5. User Authentication Response: {r_login.json().get('message')}")
    assert r_login.status_code == 200

    # 6. Creator Roles Fetch
    r_roles = session.get(f"{BASE_URL}/api/v1/creator/roles")
    roles = r_roles.json().get("roles", [])
    print(f"\n6. Creator Roles Check: Found {len(roles)} active roles.")
    assert len(roles) > 0

    # 7. Document Ingestion & RAG Quiz Generation Test
    ingest_data = {"title": "MoSPI Advanced Sampling Manual 2026", "associated_competency": "COMP_SAMPLING"}
    r_ingest = session.post(f"{BASE_URL}/api/v1/creator/upload-material", data=ingest_data)
    print(f"7. Creator Material Ingestion & RAG Response: {r_ingest.json().get('message')}")
    assert r_ingest.status_code == 200

    # 8. Learner Select Role Test
    r_select = session.post(f"{BASE_URL}/api/v1/learner/select-role", json={"user_id": "ashw_101", "role_id": "ROLE_JSO"})
    print(f"8. Learner Select Role Response: {r_select.json().get('message')}")
    assert r_select.status_code == 200

    # 9. Baseline Assessment Quiz Fetch
    r_base_q = session.get(f"{BASE_URL}/api/v1/learner/quiz/baseline/ROLE_JSO")
    base_questions = r_base_q.json().get("questions", [])
    print(f"9. Learner Baseline Diagnostic Quiz Fetch: Loaded {len(base_questions)} diagnostic questions.")

    # 10. Grade Baseline Quiz & Skill Gap Calculation
    answers = {q["id"]: q.get("answer", 0) if "answer" in q else 1 for q in base_questions}
    r_base_submit = session.post(f"{BASE_URL}/api/v1/learner/quiz/baseline/submit", json={"user_id": "ashw_101", "role_id": "ROLE_JSO", "answers": answers})
    print(f"10. Learner Baseline Quiz Grading & Skill Gap Calculation:\n{json.dumps(r_base_submit.json().get('gap_analysis'), indent=2)}")
    assert r_base_submit.status_code == 200

    # 11. Recommendations Engine Test
    r_rec = session.post(f"{BASE_URL}/api/v1/learner/recommendations", data={"user_id": "ashw_101"})
    print(f"\n11. iGOT Karmayogi Recommendation Engine Output: Found {r_rec.json().get('total_recommendations')} recommended courses/materials.")
    assert r_rec.status_code == 200

    # 12. Employee Account Deletion / Revoke Access Test
    r_del = session.delete(f"{BASE_URL}/api/v1/creator/employee/ashw_101")
    print(f"12. Revoke Employee Access & Delete Account Response: {r_del.json().get('message')}")
    assert r_del.status_code == 200

    print("\n" + "=" * 70)
    print("  ALL FULL-STACK VERIFICATION TESTS COMPLETED SUCCESSFULLY!")
    print("======================================================================\n")

if __name__ == "__main__":
    run_tests()
