from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Hugging Face AI Configuration
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
HEADERS = {"Authorization": "AIzaSyBAtMauF_DrRLDntMB7ITDTapKqKgcZOz4"}

# --- Pydantic Models for Data Validation ---

class LoginRequest(BaseModel):
    name: str      # Matches 'name' in your SQL Users table
    password: str

class CodeRequest(BaseModel):
    code: str
    user_id: int   # To link reports to a specific user

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Endpoints ---

@app.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Handles user authentication"""
    # Finding user by 'name' as defined in the LoginRequest class
    user = db.query(models.User).filter(models.User.name == request.name).first()
    
    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {"message": "Login successful", "user_id": user.user_id}

@app.post("/fix-code")
async def fix_code(request: CodeRequest, db: Session = Depends(get_db)):
    """Sends code to AI and logs data in User_Report and Solution tables"""
    
    # Direct AI call without warming up message
    ai_payload = {"inputs": f"Fix this Python code: {request.code}"}
    response = requests.post(API_URL, headers=HEADERS, json=ai_payload)
    ai_result = response.json()

    # Extracting the fixed code from the AI response
    fixed_code = ai_result[0].get("generated_text") if isinstance(ai_result, list) else "Error processing code"

    # Step 1: Save to User_Report table
    new_report = models.UserReport(
        user_id=request.user_id,
        error_type="Syntax/Logic",
        language="Python",
        code_snippet=request.code,
        error_msg="Auto-detected"
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    # Step 2: Save to Solution table
    new_solution = models.Solution(
        report_id=new_report.report_id,
        solution_text=fixed_code,
        step_to_fix="AI correction"
    )
    db.add(new_solution)
    db.commit()

    return {"fixed_code": fixed_code}

if __name__ == "__main__":
    import uvicorn
    # Running server on port 8001
    uvicorn.run(app, host="127.0.0.1", port=8001)