import os
import requests
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

app = FastAPI()

# Professional Comment: CORS setup for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Professional Comment: Create database tables in SQL Server
models.Base.metadata.create_all(bind=engine)

# --- SECURE API CONFIGURATION ---
# 1. Paste your Google AI Studio API key here
GEMINI_API_KEY = "AIzaSyBlsvU6jTSeDcHJ-xA8KP_c69q3bkdqsLk"

# 2. Use this stable URL with v1beta and gemini-pro model
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

class LoginRequest(BaseModel):
    name: str
    password: str

class CodeRequest(BaseModel):
    code: str
    user_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROUTES ---

@app.get("/")
async def root():
    # Professional Comment: Redirects direct access to the login page
    return RedirectResponse(url="/login.html")

@app.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Professional Comment: Authenticates user against SQL Server database."""
    user = db.query(models.User).filter(models.User.name == request.name).first()
    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Success", "user_id": user.user_id}

@app.post("/fix-code")
async def fix_code(request: CodeRequest, db: Session = Depends(get_db)):
    """
    Professional Comment: Core AI function to fix Python code and log it.
    """
    if not GEMINI_API_KEY:
        return {"fixed_code": "System Error: GEMINI_API_KEY not found in Windows Variables!"}

    payload = {
        "contents": [{"parts": [{"text": f"Fix this Python code. Return ONLY the code result: {request.code}"}]}]
    }
    
    try:
        response = requests.post(GEMINI_URL, json=payload, timeout=40)
        ai_data = response.json()
        
        if "candidates" in ai_data:
            fixed_code = ai_data["candidates"][0]["content"]["parts"][0]["text"]
            # Clean formatting for display in the dashboard box
            fixed_code = fixed_code.replace("```python", "").replace("```", "").strip()
        else:
            # Captures API specific errors like 404 or Invalid Key
            error_msg = ai_data.get('error', {}).get('message', 'Model Error')
            fixed_code = f"AI Error: {error_msg}"
            
    except Exception as e:
        fixed_code = f"Network Failure: {str(e)}"

    # --- SAVE TO SQL SERVER ---
    # Professional Comment: Logging the report and the solution for presentation proof
    new_report = models.UserReport(user_id=request.user_id, error_type="AI_Fix", code_snippet=request.code)
    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    new_sol = models.Solution(report_id=new_report.report_id, solution_text=fixed_code)
    db.add(new_sol)
    db.commit()

    return {"fixed_code": fixed_code}

# Professional Comment: Serve frontend static files
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")