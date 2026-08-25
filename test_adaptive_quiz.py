"""
Unit & Integration Test Suite for Adaptive Quiz Engine (CAT)
Smart India Hackathon (SIH) - AI-Enabled Learning Platform
"""

import json
import os
import unittest
from adaptive_quiz_engine import AdaptiveQuizEngine
from semantic_recommendation_engine import SemanticRecommendationEngine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "data", "db.json")

class TestAdaptiveQuizEngine(unittest.TestCase):
    def setUp(self):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            self.db_data = json.load(f)
        self.engine = AdaptiveQuizEngine(self.db_data)
        self.semantic_engine = SemanticRecommendationEngine()

    def test_experience_tier_scaling(self):
        """Verifies initial difficulty level assignment based on experience years."""
        tier1 = self.engine.get_experience_tier(1)
        tier2 = self.engine.get_experience_tier(5)
        tier3 = self.engine.get_experience_tier(10)

        self.assertEqual(tier1["tier"], 1)
        self.assertEqual(tier1["initial_level"], 1)

        self.assertEqual(tier2["tier"], 2)
        self.assertEqual(tier2["initial_level"], 2)

        self.assertEqual(tier3["tier"], 3)
        self.assertEqual(tier3["initial_level"], 2)
        print("[OK] Experience Tier Scaling test passed!")

    def test_cat_item_step_up_and_step_down(self):
        """Verifies CAT difficulty step-up (L2 -> L3) and step-down (L2 -> L1)."""
        role_id = "ROLE_JOB_001"

        # 1. Start candidate at initial level (L2 for Tier 1 mid-level role)
        q1 = self.engine.select_next_adaptive_question(role_id, history=[])
        self.assertIsNotNone(q1)

        # 2. Simulate correct answer -> Should step up to L3
        history_correct = [
            {
                "question_id": q1["question_id"],
                "competency_code": q1["competency_code"],
                "difficulty_level": 2,
                "is_correct": True
            }
        ]
        q2 = self.engine.select_next_adaptive_question(role_id, history=history_correct)
        self.assertEqual(q2["difficulty_level"], 3)
        print(f"[OK] CAT Step-Up verified: L2 -> L{q2['difficulty_level']}")

        # 3. Simulate incorrect answer -> Should step down to L1
        history_incorrect = [
            {
                "question_id": q1["question_id"],
                "competency_code": q1["competency_code"],
                "difficulty_level": 2,
                "is_correct": False
            }
        ]
        q3 = self.engine.select_next_adaptive_question(role_id, history=history_incorrect)
        self.assertEqual(q3["difficulty_level"], 1)
        print(f"[OK] CAT Step-Down verified: L2 -> L{q3['difficulty_level']}")

    def test_sub_skill_heatmap_generation(self):
        """Verifies sub-skill deficit calculation and heatmap formatting."""
        role_id = "ROLE_JOB_001"
        # Fail Q_GOV_L1_01, pass Q_FIN_L1_01
        answers = {
            "Q_GOV_L1_01": 2, # wrong option
            "Q_FIN_L1_01": 0  # correct option
        }
        heatmap = self.engine.generate_sub_skill_heatmap(role_id, answers)
        self.assertGreater(len(heatmap), 0)

        gov_sub = next((h for h in heatmap if h["sub_skill_code"] == "SUB_CSMOP"), None)
        self.assertIsNotNone(gov_sub)
        self.assertEqual(gov_sub["current_score"], 0.0)
        self.assertGreater(gov_sub["deficit_pct"], 0.0)
        print(f"[OK] Sub-Skill Heatmap verified: {gov_sub['sub_skill_name']} Deficit = {gov_sub['deficit_pct']}% (Status: {gov_sub['badge_class']})")

    def test_sub_skill_pinpoint_recommendations(self):
        """Verifies mapping of sub-skill deficits to pinpoint iGOT course modules."""
        role_id = "ROLE_JOB_001"
        answers = {"Q_GOV_L1_01": 2}
        heatmap = self.engine.generate_sub_skill_heatmap(role_id, answers)

        gap_analysis = [
            {"competency_code": "COMP_GOVERNANCE", "competency_name": "Governance & Civil Service Rules", "gap_score": 30.0}
        ]
        recs = self.semantic_engine.recommend_targeted_courses(
            user_role_title="IAS Officer",
            user_dept="DoPT",
            gap_analysis=gap_analysis,
            all_courses=self.db_data["igot_courses"],
            creator_materials=[],
            enrolled_course_ids=[],
            sub_skill_heatmap=heatmap
        )

        self.assertGreater(len(recs), 0)
        top_rec = recs[0]
        self.assertIn("pinpoint_module_section", top_rec)
        print(f"[OK] Pinpoint iGOT Recommendation verified: '{top_rec['title']}' -> {top_rec['pinpoint_module_section']}")

if __name__ == "__main__":
    unittest.main()
