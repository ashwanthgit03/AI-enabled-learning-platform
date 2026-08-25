"""
Adaptive Quiz Engine (Computerized Adaptive Testing - CAT)
Smart India Hackathon (SIH) - AI-Enabled Learning Platform

Features:
 1. Dynamic Difficulty Adjustment (CAT):
    - Starts candidate at Level 2 (Applied).
    - Step-up to Level 3 (Advanced) on correct answer.
    - Step-down to Level 1 (Foundational) on incorrect answer.
 2. Role Experience Adjustment:
    - Tier 1 (0-2 yrs), Tier 2 (3-7 yrs), Tier 3 (8+ yrs) experience adjustments.
 3. Micro-Case Study Scenario Formatter.
 4. Sub-Skill Knowledge Heatmap & Deficit Weight Calculation.
"""

from typing import List, Dict, Any, Optional

class AdaptiveQuizEngine:
    def __init__(self, db_data: Dict[str, Any]):
        self.roles = db_data.get("roles", [])
        self.quizzes = db_data.get("quizzes", {})
        self.igot_courses = db_data.get("igot_courses", [])

    def get_experience_tier(self, exp_years: int) -> Dict[str, Any]:
        """Maps candidate experience years to difficulty scaling tiers."""
        if exp_years <= 2:
            return {
                "tier": 1,
                "label": "Tier 1: Junior / Foundational Officer (0-2 Yrs)",
                "initial_level": 1,
                "preferred_distribution": [1, 2]
            }
        elif exp_years <= 7:
            return {
                "tier": 2,
                "label": "Tier 2: Mid-Level Officer (3-7 Yrs)",
                "initial_level": 2,
                "preferred_distribution": [2, 3]
            }
        else:
            return {
                "tier": 3,
                "label": "Tier 3: Senior Executive / Policy Officer (8+ Yrs)",
                "initial_level": 2,
                "preferred_distribution": [2, 3]
            }

    def select_next_adaptive_question(
        self,
        role_id: str,
        history: List[Dict[str, Any]],
        current_competency_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Implements Computerized Adaptive Testing (CAT):
        - Evaluates history to determine current target difficulty (L1, L2, or L3).
        - Selects next appropriate MCQ for the candidate.
        """
        role = next((r for r in self.roles if r["id"] == role_id), None)
        if not role and self.roles:
            role = self.roles[0]

        exp_years = role.get("experience_years", 1) if role else 1
        tier_info = self.get_experience_tier(exp_years)

        # Determine target difficulty level based on CAT response history
        if not history:
            target_level = tier_info["initial_level"]
        else:
            last_item = history[-1]
            last_was_correct = last_item.get("is_correct", False)
            last_level = last_item.get("difficulty_level", 2)

            if last_was_correct:
                target_level = min(3, last_level + 1)
            else:
                target_level = max(1, last_level - 1)

        # Target competency selection
        comps = role.get("required_competencies", []) if role else []
        if current_competency_code:
            target_comp = next((c for c in comps if c["code"] == current_competency_code), comps[0] if comps else None)
        else:
            # Pick competency with fewest answered questions
            answered_comps = [h.get("competency_code") for h in history]
            comp_counts = {c["code"]: answered_comps.count(c["code"]) for c in comps}
            sorted_comps = sorted(comp_counts.items(), key=lambda x: x[1])
            target_code = sorted_comps[0][0] if sorted_comps else "COMP_GOVERNANCE"
            target_comp = next((c for c in comps if c["code"] == target_code), None)

        comp_code = target_comp["code"] if target_comp else "COMP_GOVERNANCE"
        comp_name = target_comp["name"] if target_comp else "Governance"

        # Fetch candidate questions pool for target_code
        comp_quiz_pool = self.quizzes.get(comp_code, {}).get("baseline", []) + self.quizzes.get(comp_code, {}).get("intermediate", [])

        # Filter out already answered questions
        answered_qids = {h.get("question_id") for h in history if h.get("question_id")}
        available_pool = [q for q in comp_quiz_pool if q["id"] not in answered_qids]

        if not available_pool:
            available_pool = comp_quiz_pool

        # Select question matching target_level, fallback to adjacent levels
        matching_q = next((q for q in available_pool if q.get("difficulty_level") == target_level), None)
        if not matching_q:
            matching_q = available_pool[0] if available_pool else self._create_fallback_question(comp_code, comp_name, target_level)

        sub_skills = target_comp.get("sub_skills", []) if target_comp else []
        sub_code = matching_q.get("sub_skill_code", sub_skills[0]["code"] if sub_skills else f"SUB_{comp_code}")
        sub_name = next((s["name"] for s in sub_skills if s["code"] == sub_code), "General Operational Rules")

        return {
            "question_id": matching_q["id"],
            "competency_code": comp_code,
            "competency_name": comp_name,
            "sub_skill_code": sub_code,
            "sub_skill_name": sub_name,
            "difficulty_level": matching_q.get("difficulty_level", target_level),
            "difficulty_label": f"Level {matching_q.get('difficulty_level', target_level)} - {'Foundational' if matching_q.get('difficulty_level', target_level)==1 else ('Applied' if matching_q.get('difficulty_level', target_level)==2 else 'Advanced')}",
            "scenario_text": matching_q.get("scenario_text", f"Official Scenario for {comp_name}"),
            "question": matching_q["question"],
            "options": matching_q["options"],
            "recommended_module_id": matching_q.get("recommended_module_id", "IGOT-COURSE-001"),
            "experience_tier": tier_info["label"]
        }

    def generate_sub_skill_heatmap(
        self,
        role_id: str,
        answers: Dict[str, int]
    ) -> List[Dict[str, Any]]:
        """
        Calculates granular sub-skill knowledge gap heatmap based on quiz answers.
        """
        role = next((r for r in self.roles if r["id"] == role_id), None)
        if not role and self.roles:
            role = self.roles[0]

        sub_skill_stats = {}

        # Collect all sub-skills for the role
        for comp in role.get("required_competencies", []):
            comp_code = comp["code"]
            comp_name = comp["name"]
            target_bench = comp.get("target_score", 80.0)

            for sub in comp.get("sub_skills", []):
                sub_code = sub["code"]
                sub_name = sub["name"]
                sub_skill_stats[sub_code] = {
                    "code": sub_code,
                    "name": sub_name,
                    "competency_code": comp_code,
                    "competency_name": comp_name,
                    "target_benchmark": target_bench,
                    "total_questions": 0,
                    "correct_count": 0,
                    "weighted_score": 0.0
                }

        # Match answers against database questions
        all_questions = []
        for c_code, q_dict in self.quizzes.items():
            all_questions.extend(q_dict.get("baseline", []))
            all_questions.extend(q_dict.get("intermediate", []))

        for q in all_questions:
            q_id = q["id"]
            if q_id in answers:
                chosen_opt = answers[q_id]
                correct_opt = q["answer"]
                sub_code = q.get("sub_skill_code")

                if sub_code in sub_skill_stats:
                    stat = sub_skill_stats[sub_code]
                    stat["total_questions"] += 1
                    if chosen_opt == correct_opt:
                        stat["correct_count"] += 1

        heatmap = []
        for sub_code, stat in sub_skill_stats.items():
            total = stat["total_questions"]
            if total > 0:
                current_score = round((stat["correct_count"] / total) * 100.0, 1)
            else:
                # Default baseline estimate if un-tested
                current_score = 60.0

            target = stat["target_benchmark"]
            deficit_pct = round(max(0.0, target - current_score), 1)

            if deficit_pct <= 5.0:
                status_badge = "✅ Competent"
                badge_class = "success"
            elif deficit_pct <= 25.0:
                status_badge = "⚠️ Moderate Deficit"
                badge_class = "warning"
            else:
                status_badge = "🚨 Critical Gap"
                badge_class = "danger"

            heatmap.append({
                "sub_skill_code": sub_code,
                "sub_skill_name": stat["name"],
                "competency_code": stat["competency_code"],
                "competency_name": stat["competency_name"],
                "current_score": current_score,
                "target_benchmark": target,
                "deficit_pct": deficit_pct,
                "status_badge": status_badge,
                "badge_class": badge_class
            })

        return heatmap

    def _create_fallback_question(self, comp_code: str, comp_name: str, level: int) -> Dict[str, Any]:
        level_label = "Foundational" if level == 1 else ("Applied" if level == 2 else "Advanced")
        return {
            "id": f"Q_FALLBACK_{comp_code}_{level}",
            "competency_code": comp_code,
            "sub_skill_code": f"SUB_{comp_code}",
            "difficulty_level": level,
            "scenario_text": f"Micro-case scenario for {comp_name} ({level_label} Level).",
            "question": f"[{level_label}] Under standard guidelines for {comp_name}, what is the mandatory compliance rule?",
            "options": [
                f"Adhere strictly to official statutory guidelines for {comp_name}",
                "Execute ad-hoc manual procedure without approval",
                "Bypass audit log checks",
                "Delegate responsibility to unverified external entity"
            ],
            "answer": 0,
            "recommended_module_id": "IGOT-COURSE-001"
        }
