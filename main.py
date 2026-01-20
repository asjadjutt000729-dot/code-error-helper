from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables
models.Base.metadata.create_all(bind=engine)

# Correct Router URL for Hugging Face
API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"
# Ensure there is a space after 'Bearer'
HEADERS = {"Authorization": "Bearer AIzaSyDsfRd_DI6l5pHSbOcwsmLDeLIex_kCRrI"}

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
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful", "user_id": user.user_id}

@app.post("/fix-code")
async def fix_code(request: CodeRequest, db: Session = Depends(get_db)):
    payload = {"inputs": f"Fix Python syntax: {request.code}"}
    
    try:
        # 1. AI API Call
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        ai_result = response.json()
        
        # 2. Extract ONLY the code or the direct error message
        if isinstance(ai_result, list) and len(ai_result) > 0:
            fixed_code = ai_result[0].get("generated_text", "")
        elif isinstance(ai_result, dict) and "error" in ai_result:
            fixed_code = ai_result["error"]
        else:
            fixed_code = "Processing Error"
            
    except Exception as e:
        fixed_code = f"Connection Error: {str(e)}"

    # 3. Log to Database (Verified working)
    new_report = models.UserReport(
        user_id=request.user_id,
        error_type="Syntax",
        language="Python",
        code_snippet=request.code,
        error_msg="Analyzed"
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    new_solution = models.Solution(
        report_id=new_report.report_id,
        solution_text=fixed_code,
        step_to_fix="AI automated fix"
    )
    db.add(new_solution)
    db.commit()

    return {"fixed_code": fixed_code}

# Mount static frontend files
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    # Using double underscores for entry point
    uvicorn.run(app, host="127.0.0.1", port=8001)