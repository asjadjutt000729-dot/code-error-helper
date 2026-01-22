from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"
# Ensure there is exactly one space after 'Bearer'
# Token lazmi replace karein naye 'hf_...' token se
HEADERS = {"Authorization": "Bearer AIzaSyAExPRyuJbIE1OirutqAwesN3oauDW2s0g"}

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

@app.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == request.name).first()
    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="Invalid login")
    return {"message": "Success", "user_id": user.user_id}

@app.post("/fix-code")
async def fix_code(request: CodeRequest, db: Session = Depends(get_db)):
    payload = {
        "inputs": f"Complete this Python code: {request.code}", 
        "options": {"wait_for_model": True}
    }
    
    # Direct AI Call
    response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
    ai_result = response.json()
    
    # Taking whatever AI sends back directly
    fixed_code = str(ai_result)

    # Logging to Database (Verified working by your Green Message)
    new_report = models.UserReport(user_id=request.user_id, error_type="AI_Test", language="Python", code_snippet=request.code, error_msg="Logged")
    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    new_sol = models.Solution(report_id=new_report.report_id, solution_text=fixed_code, step_to_fix="AI Result")
    db.add(new_sol)
    db.commit()

    return {"fixed_code": fixed_code}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    # Use Port 8001
    uvicorn.run(app, host="127.0.0.1", port=8001)