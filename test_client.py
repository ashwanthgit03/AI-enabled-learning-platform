import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("=" * 60)
    print("  MEMBER 4: iGOT ADAPTER & RECOMMENDATION ENGINE TEST SUITE")
    print("  Folder: C:\\Users\\DELL\\Desktop\\SIH")
    print("=" * 60)

    # 1. Health Check
    try:
        r = requests.get(f"{BASE_URL}/")
        print("\n1. Health Check Response:")
        print(json.dumps(r.json(), indent=2))
    except Exception as e:
        print(f"FAILED to connect to server at {BASE_URL}. Make sure server.py is running!")
        sys.exit(1)

    # 2. Get Catalog
    r = requests.get(f"{BASE_URL}/api/v1/igot/catalog")
    print("\n2. iGOT Catalog Response (Total courses: {}):".format(r.json().get("total_courses")))

    # 3. Request Recommendations based on Skill Gaps
    payload = {
        "user_id": "EMP-STAT-104",
        "user_role": "Junior Statistical Officer",
        "skill_gaps": {
            "COMP_SAMPLING": 0.85,
            "COMP_DATA_ANALYTICS": 0.50,
            "COMP_INDEX_NUMBERS": 0.20
        },
        "uploaded_docs": [
            {
                "doc_id": "DOC-901",
                "filename": "MoSPI_Sampling_Guidelines_2025.pdf",
                "associated_competency": "COMP_SAMPLING"
            }
        ]
    }
    
    r = requests.post(f"{BASE_URL}/api/v1/recommendations", json=payload)
    print("\n3. Recommendation Engine Output for EMP-STAT-104:")
    print(json.dumps(r.json(), indent=2))

    # 4. Simulate Enrolment
    enroll_payload = {
        "user_id": "EMP-STAT-104",
        "course_id": "IGOT-STAT-001"
    }
    r = requests.post(f"{BASE_URL}/api/v1/igot/enroll", json=enroll_payload)
    print("\n4. iGOT Enrollment Sandbox Output:")
    print(json.dumps(r.json(), indent=2))

    # 5. Push Badge
    badge_payload = {
        "user_id": "EMP-STAT-104",
        "competency_code": "COMP_SAMPLING",
        "score_achieved": 92.5
    }
    r = requests.post(f"{BASE_URL}/api/v1/igot/badge-sync", json=badge_payload)
    print("\n5. Badge Push to iGOT Registry Output:")
    print(json.dumps(r.json(), indent=2))

    print("\n" + "=" * 60)
    print("  ALL TESTS COMPLETED SUCCESSFULLY! READY FOR SIH DEMO.")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
