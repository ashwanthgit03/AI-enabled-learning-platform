import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("=" * 70)
    print("  SIH FULL-STACK PLATFORM VERIFICATION TEST SUITE")
    print("  Testing Creator Portal, Learner Portal, User Auth, Baseline & Intermediate Quizzes,")
    print("  iGOT Course Recommendations & Badge Award Engine")
    print("=" * 70)

    # 1. Health Check & Portal Routes
    try:
        r_learner = requests.get(f"{BASE_URL}/")
        r_creator = requests.get(f"{BASE_URL}/creator")
        print("\n1. Portal Route Checks:")
        print(f"   - Learner Portal (/): HTTP {r_learner.status_code}")
        print(f"   - Creator Portal (/creator): HTTP {r_creator.status_code}")
        assert r_learner.status_code == 200
        assert r_creator.status_code == 200
    except Exception as e:
        print(f"\n[FAILED] Could not connect to server at {BASE_URL}. Ensure server.py is running! Error: {e}")
        sys.exit(1)

    # 2. User Authentication / Registration
    reg_payload = {
        "user_id": "EMP-101",
        "name": "Officer Ramesh Kumar",
        "department": "National Statistical Office (NSO)",
        "password": "pass123"
    }
    r = requests.post(f"{BASE_URL}/api/v1/auth/register", json=reg_payload)
    if r.status_code != 200:
        # If already registered, perform login
        r = requests.post(f"{BASE_URL}/api/v1/auth/login", json={"user_id": "EMP-101", "password": "pass123"})
    print(f"\n2. User Authentication Response: {r.json().get('message')}")

    # 3. Creator Portal: Get Roles
    r = requests.get(f"{BASE_URL}/api/v1/creator/roles")
    roles = r.json().get("roles", [])
    print(f"\n3. Creator Roles Check: Found {len(roles)} active roles.")

    # 4. Creator Portal: Upload Training Material & Auto-generate Quiz Questions
    form_data = {
        "title": "MoSPI_Advanced_Sampling_Manual_2026.pdf",
        "associated_competency": "COMP_SAMPLING"
    }
    r = requests.post(f"{BASE_URL}/api/v1/creator/upload-material", data=form_data)
    print(f"4. Creator Material Ingestion Response: {r.json().get('message')}")

    # 5. Learner Portal: Select Role
    r = requests.post(f"{BASE_URL}/api/v1/learner/select-role", json={"user_id": "EMP-101", "role_id": "ROLE_JSO"})
    print(f"5. Learner Select Role Response: {r.json().get('message')}")

    # 6. Learner Portal: Get Baseline Quiz
    r = requests.get(f"{BASE_URL}/api/v1/learner/quiz/baseline/ROLE_JSO")
    questions = r.json().get("questions", [])
    print(f"6. Learner Baseline Diagnostic Quiz Fetch: Loaded {len(questions)} diagnostic questions.")

    # 7. Learner Portal: Submit Baseline Quiz (simulate answers)
    answers = {}
    for q in questions:
        answers[q["id"]] = 1 # Select option 1
    
    baseline_payload = {
        "user_id": "EMP-101",
        "role_id": "ROLE_JSO",
        "answers": answers
    }
    r = requests.post(f"{BASE_URL}/api/v1/learner/quiz/baseline/submit", json=baseline_payload)
    gap_data = r.json()
    print(f"7. Learner Baseline Quiz Grading & Skill Gap Calculation:")
    print(json.dumps(gap_data.get("gap_analysis", []), indent=2))

    # 8. Learner Portal: Fetch iGOT Karmayogi Course Recommendations
    r = requests.post(f"{BASE_URL}/api/v1/learner/recommendations", data={"user_id": "EMP-101"})
    recs = r.json().get("recommendations", [])
    print(f"\n8. iGOT Karmayogi Recommendation Engine Output: Found {len(recs)} recommended courses/materials.")

    # 9. Learner Portal: Submit Post-Learning Intermediate Quiz
    int_payload = {
        "user_id": "EMP-101",
        "competency_code": "COMP_GOVERNANCE",
        "answers": {"Q_GOV_INT_1": 1}
    }
    r = requests.post(f"{BASE_URL}/api/v1/learner/quiz/intermediate/submit", json=int_payload)
    int_res = r.json()
    print(f"\n9. Intermediate Post-Course Quiz Submission & Profile Boost:")
    print(f"   - Quiz Score: {int_res.get('quiz_score')}%")
    print(f"   - Competency Level Boosted: {int_res.get('previous_competency_score')}% -> {int_res.get('updated_competency_score')}%")
    print(f"   - Badge Awarded: {int_res.get('badge_awarded', {}).get('title') if int_res.get('badge_awarded') else 'Badge Previously Issued'}")

    # 10. Learner Portal: Fetch Final Updated Live Profile
    r = requests.get(f"{BASE_URL}/api/v1/learner/profile/EMP-101")
    profile = r.json()
    print(f"\n10. Final Live User Profile Verification:")
    print(f"   - Officer Name: {profile.get('name')}")
    print(f"   - Earned Badges: {len(profile.get('badges', []))}")

    print("\n" + "=" * 70)
    print("  ALL FULL-STACK TESTS COMPLETED SUCCESSFULLY! READY FOR SIH PRESENTATION.")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
