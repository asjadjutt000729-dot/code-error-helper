import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.responses import FileResponse

app = FastAPI()

# 1. CORS Configuration: Frontend aur Backend ka rabta
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Gemini AI Configuration (Corrected your key from Jan 18)
API_KEY = "AIzaSyBzYiRDiLdhxR2YkeTMLN3JhMMbClHK94o" 
genai.configure(api_key=API_KEY)

# Using 'gemini-1.5-flash' to avoid the 404 version error
# Note: Fixed the extra 's' that was at the end of this line in your message
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Data Models for requests
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
    """Handles user authentication."""
    if request.username == "ayesha" and request.password == "1234":
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/fix-code")
async def fix_code(request: CodeRequest):
    """Sends buggy code to Gemini AI and returns fixed version."""
    try:
        prompt = f"Fix this Python code. Return ONLY the corrected code:\n\n{request.code}"
        response = model.generate_content(prompt)
        return {"fixed_code": response.text}
    except Exception as e:
        # Logs the specific error in terminal for debugging
        print(f"AI Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Serving static files for the dashboard
app.mount("/static", StaticFiles(directory="frontend"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)