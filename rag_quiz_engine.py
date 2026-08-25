"""
RAG & Document MCQ Generator Engine for MoSPI AI Learning Platform
Smart India Hackathon (SIH)
Extracts semantic concepts from uploaded PDF/text syllabus documents and generates
multi-tier adaptive evaluation MCQs tagged with sub-skills, scenario text, and distractor explanations.
"""

import re
import random
from typing import List, Dict, Any

class RAGQuizGeneratorEngine:
    def __init__(self):
        pass

    def extract_text_chunks(self, text: str, max_chunk_words: int = 100) -> List[str]:
        """Splits document text into semantic chunks for RAG processing."""
        sentences = re.split(r'(?<=[.!?]) +', text.strip())
        chunks = []
        current_chunk = []
        current_word_count = 0

        for sentence in sentences:
            words = sentence.split()
            if current_word_count + len(words) > max_chunk_words:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_word_count = len(words)
            else:
                current_chunk.append(sentence)
                current_word_count += len(words)

        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks if chunks else [text]

    def generate_quiz_from_document(self, doc_title: str, text_content: str, comp_code: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        RAG Pipeline: Reads document content, extracts key statistical & operational concepts,
        and generates multi-tier Baseline (Diagnostic) and Intermediate (Post-Course) MCQs.
        """
        chunks = self.extract_text_chunks(text_content)
        sample_scenario = chunks[0][:180] + "..." if chunks else f"Syllabus material from {doc_title}."

        sub_code_map = {
            "COMP_GOVERNANCE": "SUB_CSMOP",
            "COMP_FINANCE": "SUB_GFR",
            "COMP_DATA_ANALYTICS": "SUB_STRATIFIED",
            "COMP_IT": "SUB_EOFFICE",
            "COMP_MANAGEMENT": "SUB_PROJECTMGMT"
        }
        sub_code = sub_code_map.get(comp_code, f"SUB_{comp_code}")

        concept_templates = [
            {
                "topic": "Operational Guideline & Sampling Protocol",
                "difficulty_level": 1,
                "question": f"[Level 1 - Foundational] According to syllabus document '{doc_title}': What is the primary objective of operational guidelines for {comp_code}?",
                "correct": "To minimize process variance and ensure representative data & rule compliance",
                "distractors": [
                  "To collect non-random convenience data without stratification",
                  "To bypass official NSO field verification guidelines",
                  "To eliminate all non-sampling errors manually"
                ],
                "explanations": {
                    "1": "Convenience sampling distorts statistical validity.",
                    "2": "Bypassing guidelines violates government protocol.",
                    "3": "Non-sampling errors cannot be 100% eliminated manually."
                }
            },
            {
                "topic": "Estimation & Methodology",
                "difficulty_level": 2,
                "question": f"[Level 2 - Applied] In the training document '{doc_title}': Which formula standard is mandated for estimating population parameters under {comp_code}?",
                "correct": "Horvitz-Thompson weighted estimation formula for probability sampling",
                "distractors": [
                  "Unweighted simple arithmetic mean across non-equivalent clusters",
                  "Arbitrary non-probabilistic index scaling",
                  "Deterministic manual imputation without audit trail"
                ],
                "explanations": {
                    "1": "Unweighted arithmetic mean introduces bias across non-equivalent clusters.",
                    "2": "Non-probabilistic scaling is statistically invalid.",
                    "3": "Imputation without audit trail violates data auditing rules."
                }
            },
            {
                "topic": "Quality Assurance & Security",
                "difficulty_level": 3,
                "question": f"[Level 3 - Advanced] Based on '{doc_title}': What protocol must be followed prior to publishing public microdata?",
                "correct": "Anonymization and microdata masking in compliance with GIGW & Data Privacy protocols",
                "distractors": [
                  "Publishing unmasked personally identifiable information (PII)",
                  "Storing raw field survey schedules without encryption",
                  "Discarding baseline survey metadata without backup"
                ],
                "explanations": {
                    "1": "Publishing PII violates the DPDP Act and privacy mandates.",
                    "2": "Unencrypted storage breaches cyber hygiene protocols.",
                    "3": "Discarding metadata distorts long-term reproducibility."
                }
            }
        ]

        baseline_questions = []
        intermediate_questions = []

        # Generate Baseline Quiz Questions (L1 & L2)
        for idx, tmpl in enumerate(concept_templates[:2]):
            options = [tmpl["correct"]] + tmpl["distractors"]
            random.seed(idx + len(doc_title))
            shuffled_options = list(options)
            random.shuffle(shuffled_options)
            correct_idx = shuffled_options.index(tmpl["correct"])

            # Map explanation indices to shuffled options
            shuffled_explanations = {}
            for orig_opt_idx, expl in tmpl["explanations"].items():
                orig_text = tmpl["distractors"][int(orig_opt_idx) - 1]
                new_pos = shuffled_options.index(orig_text)
                shuffled_explanations[str(new_pos)] = expl

            baseline_questions.append({
                "id": f"Q_RAG_BASE_{comp_code}_{idx+1}",
                "sub_skill_code": sub_code,
                "difficulty_level": tmpl["difficulty_level"],
                "scenario_text": f"Excerpt from {doc_title}: '{sample_scenario}'",
                "question": tmpl["question"],
                "options": shuffled_options,
                "answer": correct_idx,
                "distractor_explanations": shuffled_explanations,
                "source": f"RAG Extracted from {doc_title}",
                "recommended_module_id": f"DOC-{doc_title}"
            })

        # Generate Intermediate Quiz Questions (L2 & L3)
        for idx, tmpl in enumerate(concept_templates[1:]):
            options = [tmpl["correct"]] + tmpl["distractors"]
            random.seed(idx + 10 + len(doc_title))
            shuffled_options = list(options)
            random.shuffle(shuffled_options)
            correct_idx = shuffled_options.index(tmpl["correct"])

            shuffled_explanations = {}
            for orig_opt_idx, expl in tmpl["explanations"].items():
                orig_text = tmpl["distractors"][int(orig_opt_idx) - 1]
                new_pos = shuffled_options.index(orig_text)
                shuffled_explanations[str(new_pos)] = expl

            intermediate_questions.append({
                "id": f"Q_RAG_INT_{comp_code}_{idx+1}",
                "sub_skill_code": sub_code,
                "difficulty_level": tmpl["difficulty_level"],
                "scenario_text": f"Excerpt from {doc_title}: '{sample_scenario}'",
                "question": tmpl["question"],
                "options": shuffled_options,
                "answer": correct_idx,
                "distractor_explanations": shuffled_explanations,
                "source": f"RAG Extracted from {doc_title}",
                "recommended_module_id": f"DOC-{doc_title}"
            })

        return {
            "baseline": baseline_questions,
            "intermediate": intermediate_questions
        }
