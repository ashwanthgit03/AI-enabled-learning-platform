# SIH Full-Stack AI Personalized Learning Platform for India's Official Statistical System
**Location**: `C:\Users\DELL\Desktop\SIH`

An end-to-end interactive learning platform built for Smart India Hackathon (SIH) connecting MoSPI roles, competency gap identification, LLM+RAG document parsing, iGOT Karmayogi course integration, diagnostic baseline quizzes, post-learning intermediate quizzes, and real-time skill profile updates.

---

## 🏛️ System Portals

### 1. Creator / Admin Portal (`/creator`)
* **URL**: `http://localhost:8000/creator`
* **Features**:
  * Define government roles (*e.g., Junior Statistical Officer, Director of Price Statistics*), eligibility criteria, required experience, and target competency benchmarks.
  * Drag & drop syllabus PDFs/documents with auto-generated LLM diagnostic quiz questions.
  * Custom MCQ Quiz Builder.
  * Department skill readiness analytics dashboard.

### 2. Learner / Government Employee Portal (`/`)
* **URL**: `http://localhost:8000/`
* **Features**:
  * **Role Selection**: Select government post and inspect eligibility benchmarks.
  * **Diagnostic Baseline Quiz**: Take initial evaluation quiz to measure current knowledge against creator targets.
  * **Skill Gap Radar**: Interactive Radar Chart & Progress Indicators showing specific gap percentages ($Target - Current = Gap$).
  * **iGOT Karmayogi Recommender**: Scraped/Indexed training feed with embedded video player modal and 1-click enrolment.
  * **Intermediate Post-Quiz**: Post-course evaluation quiz.
  * **Real-time Skill Profile Update**: Dynamic score boost, gap reduction, and live iGOT Competency Badge award.

---

## 🚀 How to Run

### 1. Start the Unified Platform Server
In your terminal inside `C:\Users\DELL\Desktop\SIH`:

```bash
python -m pip install -r requirements.txt
python -m uvicorn server:app --reload --port 8000
```
Or double-click `run.bat`!

### 2. Access Portals in Browser
* **Learner Portal**: 👉 **http://localhost:8000/**
* **Creator Portal**: 👉 **http://localhost:8000/creator**
* **Interactive API Docs**: 👉 **http://localhost:8000/docs**

### 3. Run Automated End-to-End Verification Test
In a second terminal window:
```bash
python test_full_system.py
```
