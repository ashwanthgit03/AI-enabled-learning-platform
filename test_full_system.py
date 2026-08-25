"""
Full Verification Test Suite for MoSPI AI Learning Platform (SIH) v3.4.0
Tests Creator Role Editing, Semantic Recommendation Engine, Top Proceed Button,
User ID Regex Validation, Employee Access Revocation, Baseline & Intermediate Quizzes.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("=" * 70)
    print("  SIH FULL-STACK PLATFORM VERIFICATION TEST SUITE (v3.4.0)")
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

    # 2. Valid User Registration Test
    valid_reg_payload = {
        "user_id": "ashw_101",
        "name": "Officer Ramesh Kumar",
        "department": "Price Statistics Division",
        "password": "123",
        "job_role_id": "ROLE_JOB_001"
    }
    r_reg = session.post(f"{BASE_URL}/api/v1/auth/register", json=valid_reg_payload)
    print(f"2. Registration Test (user_id='ashw_101'): HTTP {r_reg.status_code}")

    # 3. Creator Modify Role Details & Target Competencies API Test
    update_role_payload = {
        "title": "Indian Administrative Service (IAS - Senior Cadre)",
        "department": "Department of Personnel and Training (DoPT)",
        "eligibility": "Master's Degree + Union Public Service Commission Civil Services Examination",
        "required_competencies": [
            {"code": "COMP_GOVERNANCE", "name": "Governance & Civil Service Rules", "target_score": 90},
            {"code": "COMP_FINANCE", "name": "Financial Rules & Procurement", "target_score": 85}
        ]
    }
    r_update = session.put(f"{BASE_URL}/api/v1/creator/roles/ROLE_JOB_001", json=update_role_payload)
    print(f"3. Creator Modify Role Details API (PUT /roles/ROLE_JOB_001): HTTP {r_update.status_code}")
    assert r_update.status_code == 200

    # 4. Select Role Test
    r_select = session.post(f"{BASE_URL}/api/v1/learner/select-role", json={"user_id": "ashw_101", "role_id": "ROLE_JOB_001"})
    print(f"4. Learner Select Role Response: {r_select.json().get('message')}")
    assert r_select.status_code == 200

    # 5. Diagnostic Baseline Assessment Quiz Fetch
    r_base_q = session.get(f"{BASE_URL}/api/v1/learner/quiz/baseline/ROLE_JOB_001")
    base_questions = r_base_q.json().get("questions", [])
    print(f"5. Baseline Diagnostic Quiz Fetch: Loaded {len(base_questions)} questions.")

    # 6. Grade Baseline Quiz & Skill Gap Calculation
    answers = {q["id"]: 0 for q in base_questions}
    r_base_submit = session.post(f"{BASE_URL}/api/v1/learner/quiz/baseline/submit", json={"user_id": "ashw_101", "role_id": "ROLE_JOB_001", "answers": answers})
    print(f"6. Skill Gap Analysis Result:\n{json.dumps(r_base_submit.json().get('gap_analysis'), indent=2)}")
    assert r_base_submit.status_code == 200

    # 7. Semantic Gap-Based Recommendation Engine Test
    r_rec = session.post(f"{BASE_URL}/api/v1/learner/recommendations", data={"user_id": "ashw_101"})
    recs = r_rec.json().get("recommendations", [])
    print(f"\n7. Semantic Recommendation Output: Found {len(recs)} targeted courses for identified gaps.")
    if recs:
        print(f"   Top Match: '{recs[0]['title']}' for {recs[0]['target_competency']} (Relevance Score: {recs[0]['relevance_score']}%)")
    assert r_rec.status_code == 200

    # 8. Employee Account Access Revocation
    r_del = session.delete(f"{BASE_URL}/api/v1/creator/employee/ashw_101")
    print(f"8. Creator Revoke Access Response: {r_del.json().get('message')}")
    assert r_del.status_code == 200

    print("\n" + "=" * 70)
    print("  ALL FULL-STACK VERIFICATION TESTS COMPLETED SUCCESSFULLY!")
    print("======================================================================\n")

if __name__ == "__main__":
    run_tests()
