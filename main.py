import os
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.responses import FileResponse

app = FastAPI()

# 1. CORS Configuration: Allows frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Gemini AI Setup: Using 1.5-flash to fix the 404 Model Not Found error
API_KEY = "AIzaSyBzYiRDiLdhxR2YkeTMLN3JhMMbClHK94o" # Replace with your key from Google AI Studio
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Data Models for incoming requests
class LoginRequest(BaseModel):
    """Model for user login credentials."""
    username: str
    password: str

class CodeRequest(BaseModel):
    """Model for code repair requests."""
    code: str

# 4. Routes (Endpoints)

@app.get("/")
async def read_login():
    """Serves the login page by default."""
    return FileResponse('frontend/login.html')

@app.post("/login")
async def login(request: LoginRequest):
    """Handles user authentication and fixes the 'Not Found' error."""
    if request.username == "ayesha" and request.password == "1234":
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/fix-code")
async def fix_code(request: CodeRequest):
    """Sends buggy code to Gemini AI and returns the fixed version."""
    try:
        prompt = f"Fix this Python code. Return ONLY the corrected code:\n\n{request.code}"
        response = model.generate_content(prompt)
        return {"fixed_code": response.text}
    except Exception as e:
        print(f"AI Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Serving the dashboard and other static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)