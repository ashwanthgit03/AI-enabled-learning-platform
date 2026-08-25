"""
AI-Enabled Personalized Learning Platform for India's Official Statistical System
Smart India Hackathon (SIH) - Full Stack Server with RAG Quiz Engine
Powering: 
 1. Creator / Admin Portal (/creator)
 2. Learner / Government Employee Portal (/)
Location: C:/Users/DELL/Desktop/SIH
"""

import json
import os
import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from pydantic import BaseModel, Field

# Import iGOT Scraper Module & RAG Quiz Engine
from igot_scraper import IGOTKarmayogiScraper
from rag_quiz_engine import RAGQuizGeneratorEngine

app = FastAPI(
    title="GovLearn AI Platform (SIH)",
    description="Full-stack AI learning platform with Creator Portal & Learner Portal connecting to iGOT Karmayogi ecosystem.",
    version="3.0.0"
)

# Enable CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATIC_DIR = os.path.join(BASE_DIR, "static")
DB_FILE = os.path.join(DATA_DIR, "db.json")

rag_engine = RAGQuizGeneratorEngine()

# Helper functions for JSON database persistence
def read_db() -> Dict[str, Any]:
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"roles": [], "quizzes": {}, "igot_courses": [], "creator_uploaded_materials": [], "users": {}}

def write_db(data: Dict[str, Any]):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# -------------------------------------------------------------------
# PYDANTIC SCHEMAS
# -------------------------------------------------------------------
class RegisterRequest(BaseModel):
    user_id: str = Field(..., example="EMP-102")
    name: str = Field(..., example="Priya Sharma")
    department: str = Field(..., example="Price Statistics Division")
    password: str = Field(..., example="pass123")

class LoginRequest(BaseModel):
    user_id: str = Field(..., example="EMP-102")
    password: str = Field(..., example="pass123")

class CompetencyRequirement(BaseModel):
    code: str
    name: str
    target_score: float = Field(..., ge=1, le=100)

class CreateRoleRequest(BaseModel):
    id: str
    title: str
    department: str
    eligibility: str
    experience_years: int
    description: str
    required_competencies: List[CompetencyRequirement]

class CreateIGOTCourseRequest(BaseModel):
    course_id: str
    title: str
    provider: str
    competency_code: str
    igot_url: str
    description: str
    embed_video_url: Optional[str] = "https://www.youtube.com/embed/3E16_f6V4mI"

class SelectRoleRequest(BaseModel):
    user_id: str
    role_id: str

class BaselineSubmitRequest(BaseModel):
    user_id: str
    role_id: str
    answers: Dict[str, int]

class IntermediateSubmitRequest(BaseModel):
    user_id: str
    competency_code: str
    answers: Dict[str, int]

class EnrollRequest(BaseModel):
    user_id: str
    course_id: str

class AddQuizQuestionRequest(BaseModel):
    competency_code: str
    quiz_type: str = Field(..., example="baseline")
    question: str
    options: List[str]
    answer: int

# -------------------------------------------------------------------
# STATIC FILES & PORTAL ROUTES
# -------------------------------------------------------------------
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", tags=["Portals"])
def serve_learner_portal():
    """Serves the Learner / Government Employee Portal."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"message": "Learner portal index.html not found"}, status_code=404)

@app.get("/creator", tags=["Portals"])
def serve_creator_portal():
    """Serves the Creator / Admin Portal."""
    creator_path = os.path.join(STATIC_DIR, "creator.html")
    if os.path.exists(creator_path):
        return FileResponse(creator_path)
    return JSONResponse({"message": "Creator portal creator.html not found"}, status_code=404)

@app.get("/static/docs/{doc_id}", tags=["Documents"])
def serve_document_viewer(doc_id: str):
    """Serves interactive HTML document reader for creator uploaded training materials."""
    db = read_db()
    materials = db.get("creator_uploaded_materials", [])
    doc = next((m for m in materials if m["id"] == doc_id), None)
    
    title = doc["title"] if doc else f"MoSPI Technical Training Document ({doc_id})"
    summary = doc["summary"] if doc else "Official MoSPI statistical training guidelines and operational procedures."
    comp = doc["associated_competency"] if doc else "COMP_SAMPLING"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>{title} - MoSPI Document Viewer</title>
      <link rel="stylesheet" href="/static/styles.css">
    </head>
    <body style="background: #f5f7fb; color: #172033; padding: 2rem; font-family: sans-serif;">
      <div class="glass-card" style="max-width: 800px; margin: 0 auto; padding: 2.5rem; background: #ffffff;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
          <span style="font-size: 0.8rem; background: #eff6ff; color: #2563eb; padding: 0.3rem 0.6rem; border-radius: 4px; font-weight: 700;">📄 OFFICIAL CREATOR SYLLABUS DOCUMENT</span>
          <span style="font-size: 0.8rem; color: #64748b;">Document ID: {doc_id}</span>
        </div>
        
        <h1 style="color: #172033; font-size: 1.8rem; margin-bottom: 0.5rem;">{title}</h1>
        <p style="color: #ea580c; font-size: 0.95rem; margin-bottom: 1.5rem; font-weight: 600;">Associated Target Competency: <strong>{comp}</strong></p>
        
        <div style="background: #f8fafc; border-radius: 12px; padding: 1.5rem; border: 1px solid #edf0f4; margin-bottom: 1.5rem;">
          <h3 style="color: #1e3a8a; margin-bottom: 0.75rem;">📘 Syllabus Summary & RAG Generated Evaluation Guidelines</h3>
          <p style="color: #475569; font-size: 1rem; line-height: 1.7;">{summary}</p>
        </div>

        <div style="background: #ecfdf5; border-radius: 12px; padding: 1.5rem; border: 1px solid #a7f3d0; margin-bottom: 2rem;">
          <h4 style="color: #16a34a; margin-bottom: 0.5rem;">💡 Key Learning Objectives & AI RAG Assessment</h4>
          <ul style="color: #475569; font-size: 0.95rem; line-height: 1.6; padding-left: 1.2rem;">
            <li>Standardized data collection methodologies according to NSO guidelines</li>
            <li>Error auditing and quality assurance standards for official statistics</li>
            <li>Compliance with Indian Government Data Governance Protocols</li>
          </ul>
        </div>

        <div style="text-align: center;">
          <a href="/" class="btn btn-primary" style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.8rem 1.5rem;">
            ➔ Return to Learner Portal & Take Evaluation Quiz
          </a>
        </div>
      </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# -------------------------------------------------------------------
# USER AUTHENTICATION & REGISTRATION APIs
# -------------------------------------------------------------------
@app.post("/api/v1/auth/register", tags=["Authentication"])
def register_user(req: RegisterRequest):
    """Registers a new government employee and persists account in database."""
    db = read_db()
    users = db.get("users", {})
    
    uid = req.user_id.strip()
    if uid in users:
        raise HTTPException(status_code=400, detail=f"User ID '{uid}' already registered. Please login instead.")
        
    user_record = {
        "user_id": uid,
        "name": req.name.strip(),
        "department": req.department.strip(),
        "password": req.password,
        "created_at": datetime.datetime.now().isoformat(),
        "selected_role_id": None,
        "current_scores": {},
        "enrolled_courses": [],
        "completed_courses": [],
        "badges": []
    }
    
    users[uid] = user_record
    db["users"] = users
    write_db(db)
    
    return {
        "status": "SUCCESS",
        "message": f"Account created for Officer {req.name} ({uid}). Saved permanently to database.",
        "user": user_record
    }

@app.post("/api/v1/auth/login", tags=["Authentication"])
def login_user(req: LoginRequest):
    """Authenticates existing user with user_id and password."""
    db = read_db()
    users = db.get("users", {})
    
    uid = req.user_id.strip()
    user = users.get(uid)
    if not user:
        raise HTTPException(status_code=404, detail=f"User ID '{uid}' not found. Please register first.")
        
    if user.get("password") and user.get("password") != req.password:
        raise HTTPException(status_code=401, detail="Incorrect password. Please try again.")
        
    return {
        "status": "SUCCESS",
        "message": f"Welcome back, {user.get('name')}!",
        "user": user
    }

# -------------------------------------------------------------------
# CREATOR PORTAL APIs
# -------------------------------------------------------------------
@app.get("/api/v1/creator/roles", tags=["Creator Portal"])
def get_all_creator_roles():
    db = read_db()
    return {"status": "success", "roles": db.get("roles", [])}

@app.post("/api/v1/creator/roles", tags=["Creator Portal"])
def create_role(req: CreateRoleRequest):
    """Creator endpoint to add a new government role with required eligibility & competencies."""
    db = read_db()
    roles = db.get("roles", [])
    
    for r in roles:
        if r["id"] == req.id:
            raise HTTPException(status_code=400, detail=f"Role with ID '{req.id}' already exists.")
            
    new_role = req.dict()
    roles.append(new_role)
    db["roles"] = roles
    write_db(db)
    
    return {"status": "SUCCESS", "message": f"Role '{req.title}' created successfully by Creator.", "role": new_role}

@app.post("/api/v1/creator/igot/add", tags=["Creator Portal"])
def add_igot_course(req: CreateIGOTCourseRequest):
    """Creator endpoint to index or add custom iGOT Karmayogi course."""
    db = read_db()
    courses = db.get("igot_courses", [])
    
    for c in courses:
        if c["course_id"] == req.course_id:
            raise HTTPException(status_code=400, detail=f"Course with ID '{req.course_id}' already exists.")
            
    new_course = req.dict()
    new_course["competency_name"] = req.competency_code
    new_course["duration"] = "10 Hours"
    new_course["rating"] = 4.8
    
    courses.append(new_course)
    db["igot_courses"] = courses
    write_db(db)
    
    return {"status": "SUCCESS", "message": f"iGOT Course '{req.title}' added to database.", "course": new_course}

@app.post("/api/v1/creator/upload-material", tags=["Creator Portal"])
def upload_learning_material(
    title: str = Form(...),
    associated_competency: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    """
    Creator endpoint to upload training document (PDF/DOCX).
    RAG & AI Quiz Generator Engine reads document text and automatically generates
    both Starting Baseline MCQs and Intermediate Post-Course Evaluation MCQs!
    """
    db = read_db()
    materials = db.get("creator_uploaded_materials", [])
    
    filename = file.filename if file else title
    doc_id = f"DOC-{len(materials) + 101}"
    
    doc_text = f"Syllabus and operational guidelines for {title} under competency {associated_competency}."
    if file:
        try:
            content_bytes = file.file.read()
            doc_text = content_bytes.decode('utf-8', errors='ignore')
        except Exception:
            pass

    new_material = {
        "id": doc_id,
        "title": filename,
        "associated_competency": associated_competency,
        "uploaded_at": datetime.datetime.now().isoformat(),
        "summary": f"Uploaded training document '{title}' for competency {associated_competency}."
    }
    materials.append(new_material)
    db["creator_uploaded_materials"] = materials
    
    # Run RAG Quiz Engine to generate MCQs automatically from document content
    rag_results = rag_engine.generate_quiz_from_document(filename, doc_text, associated_competency)
    
    quizzes = db.get("quizzes", {})
    if associated_competency not in quizzes:
        quizzes[associated_competency] = {"baseline": [], "intermediate": []}
        
    quizzes[associated_competency]["baseline"].extend(rag_results["baseline"])
    quizzes[associated_competency]["intermediate"].extend(rag_results["intermediate"])
    db["quizzes"] = quizzes
    
    write_db(db)
    return {
        "status": "SUCCESS",
        "message": f"Material '{filename}' ingested successfully! RAG Engine generated {len(rag_results['baseline'])} Baseline questions & {len(rag_results['intermediate'])} Intermediate questions.",
        "material": new_material,
        "rag_generated_quizzes": rag_results
    }

@app.post("/api/v1/creator/quiz/add", tags=["Creator Portal"])
def add_custom_quiz_question(req: AddQuizQuestionRequest):
    """Creator endpoint to manually add custom MCQs to any competency baseline or intermediate quiz."""
    db = read_db()
    quizzes = db.get("quizzes", {})
    
    if req.competency_code not in quizzes:
        quizzes[req.competency_code] = {"baseline": [], "intermediate": []}
        
    q_list = quizzes[req.competency_code].get(req.quiz_type, [])
    new_q_id = f"Q_CUSTOM_{len(q_list) + 1}"
    
    new_question = {
        "id": new_q_id,
        "question": req.question,
        "options": req.options,
        "answer": req.answer
    }
    q_list.append(new_question)
    quizzes[req.competency_code][req.quiz_type] = q_list
    db["quizzes"] = quizzes
    write_db(db)
    
    return {"status": "SUCCESS", "message": f"Custom question added to {req.competency_code} {req.quiz_type} quiz.", "question": new_question}

@app.get("/api/v1/creator/employees", tags=["Creator Portal"])
def get_registered_employees():
    """Returns list of all registered government employees stored in creator database."""
    db = read_db()
    users = db.get("users", {})
    roles = db.get("roles", [])

    role_map = {r["id"]: r["title"] for r in roles}

    employee_list = []
    for u_id, u in users.items():
        role_title = role_map.get(u.get("selected_role_id"), "None Selected")
        employee_list.append({
            "user_id": u_id,
            "name": u.get("name"),
            "department": u.get("department", "MoSPI Department"),
            "created_at": u.get("created_at", "N/A"),
            "selected_role_title": role_title,
            "badge_count": len(u.get("badges", [])),
            "enrolled_count": len(u.get("enrolled_courses", []))
        })

    return {"status": "success", "total": len(employee_list), "employees": employee_list}

@app.get("/api/v1/creator/analytics", tags=["Creator Portal"])
def get_creator_analytics():
    """Department skill gap analytics dashboard for Creators/Admins."""
    db = read_db()
    users = db.get("users", {})
    roles = db.get("roles", [])
    
    total_employees = len(users)
    active_roles_count = len(roles)
    
    competency_totals: Dict[str, List[float]] = {}
    for user_data in users.values():
        scores = user_data.get("current_scores", {})
        for comp, score in scores.items():
            if comp not in competency_totals:
                competency_totals[comp] = []
            competency_totals[comp].append(score)
            
    competency_averages = {
        comp: round(sum(scores)/len(scores), 1) for comp, scores in competency_totals.items()
    } if competency_totals else {}

    return {
        "total_employees": total_employees,
        "total_active_roles": active_roles_count,
        "total_uploaded_materials": len(db.get("creator_uploaded_materials", [])),
        "department_competency_averages": competency_averages
    }

# -------------------------------------------------------------------
# iGOT KARMAYOGI SCRAPER & REFRESH API
# -------------------------------------------------------------------
@app.get("/api/v1/igot/catalog", tags=["iGOT Sandbox"])
def get_igot_catalog():
    """Returns the full catalog of indexed iGOT courses."""
    db = read_db()
    courses = db.get("igot_courses", [])
    return {"status": "success", "total_courses": len(courses), "courses": courses}

@app.post("/api/v1/igot/scrape-refresh", tags=["iGOT Web Scraper"])
def refresh_igot_courses():
    """Triggers live web scraping of igotkarmayogi.gov.in and indexes official courses."""
    scraper = IGOTKarmayogiScraper()
    fresh_courses = scraper.scrape_igot_statistical_courses()
    
    db = read_db()
    db["igot_courses"] = fresh_courses
    write_db(db)
    
    return {
        "status": "SUCCESS",
        "message": f"Successfully scraped and indexed {len(fresh_courses)} official government training courses from igotkarmayogi.gov.in",
        "courses": fresh_courses
    }

# -------------------------------------------------------------------
# LEARNER PORTAL APIs
# -------------------------------------------------------------------
@app.get("/api/v1/learner/roles", tags=["Learner Portal"])
def get_learner_roles():
    """Returns available government roles and eligibility benchmarks for learners to choose from."""
    db = read_db()
    return {"status": "success", "roles": db.get("roles", [])}

@app.post("/api/v1/learner/select-role", tags=["Learner Portal"])
def select_user_role(req: SelectRoleRequest):
    """Learner selects their government role."""
    db = read_db()
    users = db.get("users", {})
    roles = db.get("roles", [])
    
    role = next((r for r in roles if r["id"] == req.role_id), None)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found.")
        
    user_data = users.get(req.user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found. Please log in.")
        
    user_data["selected_role_id"] = req.role_id
    users[req.user_id] = user_data
    db["users"] = users
    write_db(db)
    
    return {"status": "SUCCESS", "message": f"Role selected: {role['title']}", "role": role, "user": user_data}

@app.get("/api/v1/learner/quiz/baseline/{role_id}", tags=["Learner Portal"])
def get_baseline_quiz(role_id: str):
    """Generates diagnostic baseline assessment quiz combining Creator MCQs & RAG Document MCQs."""
    db = read_db()
    roles = db.get("roles", [])
    quizzes = db.get("quizzes", {})
    
    role = next((r for r in roles if r["id"] == role_id), None)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found.")
        
    questions = []
    for comp in role["required_competencies"]:
        comp_code = comp["code"]
        comp_name = comp["name"]
        comp_quizzes = quizzes.get(comp_code, {}).get("baseline", [])
        
        for q in comp_quizzes:
            questions.append({
                "id": q["id"],
                "competency_code": comp_code,
                "competency_name": comp_name,
                "question": q["question"],
                "options": q["options"],
                "source": q.get("source", "Creator Benchmark")
            })
            
    return {
        "status": "success",
        "role_title": role["title"],
        "total_questions": len(questions),
        "questions": questions
    }

@app.post("/api/v1/learner/quiz/baseline/submit", tags=["Learner Portal"])
def submit_baseline_quiz(req: BaselineSubmitRequest):
    """
    Grades diagnostic baseline quiz, updates user's baseline scores,
    and calculates skill gaps against Creator's required benchmark target scores.
    """
    db = read_db()
    roles = db.get("roles", [])
    quizzes = db.get("quizzes", {})
    users = db.get("users", {})
    
    role = next((r for r in roles if r["id"] == req.role_id), None)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found.")
        
    user_data = users.get(req.user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found.")

    competency_results: Dict[str, Dict[str, int]] = {}
    for comp in role["required_competencies"]:
        competency_results[comp["code"]] = {"correct": 0, "total": 0}
        
    for comp in role["required_competencies"]:
        comp_code = comp["code"]
        comp_quizzes = quizzes.get(comp_code, {}).get("baseline", [])
        
        for q in comp_quizzes:
            q_id = q["id"]
            if q_id in req.answers:
                competency_results[comp_code]["total"] += 1
                if req.answers[q_id] == q["answer"]:
                    competency_results[comp_code]["correct"] += 1

    current_scores = {}
    gap_analysis = []
    
    for comp in role["required_competencies"]:
        comp_code = comp["code"]
        comp_name = comp["name"]
        target = comp["target_score"]
        
        res = competency_results.get(comp_code, {"correct": 0, "total": 1})
        tot = res["total"] if res["total"] > 0 else 1
        score_pct = round((res["correct"] / tot) * 100, 1)
        
        gap = max(0.0, round(target - score_pct, 1))
        
        current_scores[comp_code] = score_pct
        gap_analysis.append({
            "competency_code": comp_code,
            "competency_name": comp_name,
            "current_score": score_pct,
            "target_benchmark": target,
            "gap_score": gap,
            "gap_percentage": round((gap / target) * 100, 1) if target > 0 else 0,
            "needs_training": gap > 5.0
        })
        
    user_data["selected_role_id"] = req.role_id
    user_data["current_scores"] = current_scores
    users[req.user_id] = user_data
    db["users"] = users
    write_db(db)
    
    return {
        "status": "SUCCESS",
        "user_id": req.user_id,
        "role_title": role["title"],
        "current_scores": current_scores,
        "gap_analysis": gap_analysis
    }

@app.post("/api/v1/learner/recommendations", tags=["Learner Portal"])
def get_recommendations_and_igot_scraping(user_id: str = Form(...)):
    """
    Dynamically indexes iGOT Karmayogi web catalog and creator materials,
    matching identified competency gaps to recommend courses.
    """
    db = read_db()
    users = db.get("users", {})
    roles = db.get("roles", [])
    igot_courses = db.get("igot_courses", [])
    creator_materials = db.get("creator_uploaded_materials", [])
    
    user = users.get(user_id)
    if not user or not user.get("selected_role_id"):
        raise HTTPException(status_code=400, detail="User or selected role not found. Complete baseline assessment first.")
        
    role = next((r for r in roles if r["id"] == user["selected_role_id"]), None)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found.")
        
    current_scores = user.get("current_scores", {})
    recommendations = []
    
    for comp in role["required_competencies"]:
        comp_code = comp["code"]
        comp_name = comp["name"]
        target = comp["target_score"]
        current = current_scores.get(comp_code, 0.0)
        gap = max(0.0, target - current)
        
        if gap <= 5.0:
            continue
            
        matching_igot = [c for c in igot_courses if c.get("competency_code") == comp_code]
        for course in matching_igot:
            recommendations.append({
                "id": course["course_id"],
                "type": "iGOT_KARMAYOGI_COURSE",
                "title": course["title"],
                "provider": course["provider"],
                "target_competency": comp_name,
                "competency_code": comp_code,
                "gap_score": gap,
                "urgency": "HIGH" if gap >= 30.0 else "MEDIUM",
                "duration": course["duration"],
                "rating": course["rating"],
                "action_url": course["igot_url"],
                "embed_video_url": course.get("embed_video_url", ""),
                "description": course["description"],
                "is_enrolled": course["course_id"] in user.get("enrolled_courses", [])
            })
            
        matching_docs = [d for d in creator_materials if d.get("associated_competency") == comp_code]
        for doc in matching_docs:
            recommendations.append({
                "id": doc["id"],
                "type": "CREATOR_DOCUMENT_PDF",
                "title": doc["title"],
                "provider": "MoSPI Creator Module (Internal Document)",
                "target_competency": comp_name,
                "competency_code": comp_code,
                "gap_score": gap,
                "urgency": "HIGH" if gap >= 30.0 else "MEDIUM",
                "duration": "Self-paced",
                "rating": 5.0,
                "action_url": f"/static/docs/{doc['id']}",
                "embed_video_url": "https://www.youtube.com/embed/3E16_f6V4mI",
                "description": doc["summary"],
                "is_enrolled": True
            })

    recommendations.sort(key=lambda x: x["gap_score"], reverse=True)

    return {
        "status": "success",
        "user_id": user_id,
        "role_title": role["title"],
        "total_recommendations": len(recommendations),
        "recommendations": recommendations
    }

@app.post("/api/v1/learner/igot/enroll", tags=["Learner Portal"])
def enroll_learner_course(req: EnrollRequest):
    """Enrolls learner in an iGOT course."""
    db = read_db()
    users = db.get("users", {})
    user = users.get(req.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
        
    if req.course_id not in user.get("enrolled_courses", []):
        user["enrolled_courses"].append(req.course_id)
        users[req.user_id] = user
        db["users"] = users
        write_db(db)
        
    return {"status": "SUCCESS", "message": f"Enrolled in course {req.course_id} on iGOT Karmayogi."}

@app.get("/api/v1/learner/quiz/intermediate/{competency_code}", tags=["Learner Portal"])
def get_intermediate_quiz(competency_code: str):
    """Returns post-learning intermediate evaluation quiz combining Creator MCQs & RAG Document MCQs."""
    db = read_db()
    quizzes = db.get("quizzes", {})
    comp_quizzes = quizzes.get(competency_code, {}).get("intermediate", [])
    
    if not comp_quizzes:
        comp_quizzes = [{
            "id": f"Q_INT_GENERIC_{competency_code}",
            "question": f"Post-Learning Check for {competency_code}: Did you master the key operational guidelines?",
            "options": ["Yes, fully mastered", "Needs basic review", "Incomplete overview", "Not applicable"],
            "answer": 0
        }]
        
    return {
        "status": "success",
        "competency_code": competency_code,
        "total_questions": len(comp_quizzes),
        "questions": comp_quizzes
    }

@app.post("/api/v1/learner/quiz/intermediate/submit", tags=["Learner Portal"])
def submit_intermediate_quiz(req: IntermediateSubmitRequest):
    """
    Grades intermediate post-learning quiz, updates employee's competency score,
    reduces knowledge gap towards target benchmark, and awards iGOT Competency Badge!
    """
    db = read_db()
    quizzes = db.get("quizzes", {})
    users = db.get("users", {})
    
    user = users.get(req.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
        
    comp_quizzes = quizzes.get(req.competency_code, {}).get("intermediate", [])
    correct = 0
    total = len(comp_quizzes) if comp_quizzes else 1
    
    for q in comp_quizzes:
        q_id = q["id"]
        if q_id in req.answers and req.answers[q_id] == q["answer"]:
            correct += 1
            
    quiz_score = round((correct / total) * 100, 1)
    
    current_scores = user.get("current_scores", {})
    previous_score = current_scores.get(req.competency_code, 40.0)
    
    new_score = min(95.0, max(previous_score, previous_score + (quiz_score * 0.45)))
    current_scores[req.competency_code] = round(new_score, 1)
    user["current_scores"] = current_scores
    
    badge_awarded = None
    if new_score >= 70.0:
        badge_code = f"BADGE-IGOT-{req.competency_code}"
        if badge_code not in [b["code"] for b in user.get("badges", [])]:
            badge_awarded = {
                "code": badge_code,
                "competency_code": req.competency_code,
                "title": f"Certified iGOT Specialist in {req.competency_code}",
                "issued_at": datetime.datetime.now().isoformat()
            }
            user["badges"].append(badge_awarded)
            
    users[req.user_id] = user
    db["users"] = users
    write_db(db)
    
    return {
        "status": "SUCCESS",
        "quiz_score": quiz_score,
        "previous_competency_score": previous_score,
        "updated_competency_score": round(new_score, 1),
        "gap_reduced_by": round(new_score - previous_score, 1),
        "badge_awarded": badge_awarded,
        "message": "Knowledge gap updated successfully! Your updated skill level is live on your profile."
    }

@app.get("/api/v1/learner/profile/{user_id}", tags=["Learner Portal"])
def get_user_profile(user_id: str):
    """Returns real-time user profile, current scores, target benchmarks, and badges."""
    db = read_db()
    users = db.get("users", {})
    roles = db.get("roles", [])
    
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
        
    role = next((r for r in roles if r["id"] == user.get("selected_role_id")), None)
    
    competency_summary = []
    if role:
        for comp in role["required_competencies"]:
            code = comp["code"]
            name = comp["name"]
            target = comp["target_score"]
            current = user.get("current_scores", {}).get(code, 0.0)
            gap = max(0.0, round(target - current, 1))
            
            competency_summary.append({
                "code": code,
                "name": name,
                "target_benchmark": target,
                "current_score": current,
                "gap": gap,
                "status": "COMPETENT" if gap <= 5.0 else "GAP_IDENTIFIED"
            })
            
    return {
        "user_id": user_id,
        "name": user.get("name"),
        "department": user.get("department"),
        "role": role,
        "competencies": competency_summary,
        "enrolled_courses": user.get("enrolled_courses", []),
        "badges": user.get("badges", [])
    }