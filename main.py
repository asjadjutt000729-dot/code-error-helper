import os
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Add CORS (Cross-Origin Resource Sharing) middleware to the application
# This is required to allow the frontend (running on the browser) to communicate with the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"] permits requests from any domain or origin
    allow_origins=["*"], 
    
    # allow_credentials=True enables the server to support user-based authentication or cookies
    allow_credentials=True,
    
    # allow_methods=["*"] allows all HTTP methods (GET, POST, etc.) for full functionality
    allow_methods=["*"],
    
    # allow_headers=["*"] permits any custom headers to be sent in the API request
    allow_headers=["*"],
)

# 1. Gemini API Configuration
genai.configure(api_key="AIzaSyD9_z1a9MIDAIIr1gY_Ez9DrEM2_rskQLA")
model = genai.GenerativeModel('gemini-pro')

# Data model for code fix requests
class CodeRequest(BaseModel):
    code: str

# 2. LOGIN LOGIC: Static user for demonstration
@app.post("/login")
async def login(username: str = Body(...), password: str = Body(...)):
    # Checking against your credentials in screenshot
    if username == "ayesha" and password == "1234":
        return {"message": "Login successful", "redirect": "/static/index.html"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

# 3. AI CODE FIX ENDPOINT
@app.post("/fix-code")
async def fix_code(request: CodeRequest):
    try:
        prompt = f"Fix this Python code. Return ONLY the corrected code:\n\n{request.code}"
        response = model.generate_content(prompt)
        return {"fixed_code": response.text}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="AI Error")

# 4. SERVING STATIC FILES (Login & Dashboard)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)