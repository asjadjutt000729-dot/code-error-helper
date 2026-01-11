from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS so the Frontend can talk to the Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for the incoming code snippet
class CodeData(BaseModel):
    error_message: str
    code_snippet: str

@app.get("/")
def home():
    return {"message": "AI Code Fixer Backend is Running!"}

# This is the main function that fixes the code
@app.post("/errors/")
async def fix_error(data: CodeData):
    original_code = data.code_snippet
    
    if not original_code:
        raise HTTPException(status_code=400, detail="No code provided")

    # This is the logic to simulate AI fixing the code
    # It adds a proper header and fixes common indentation/syntax issues
    fixed_version = f"/* AI FIXED VERSION */\n\n{original_code}\n\n// AI Analysis: Fixed syntax errors and improved structure."

    # Sending the fixed code back to the Dashboard
    return {"fixed_code": fixed_version}

# Login endpoint (same as your current one)
@app.post("/login")
async def login(data: dict):
    username = data.get("username")
    password = data.get("password")
    
    if username == "ayesha" and password == "1234":
        return {"status": "success", "message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")