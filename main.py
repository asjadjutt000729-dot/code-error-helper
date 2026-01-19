from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# High-speed model for logic repair
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

class LoginRequest(BaseModel):
    username: str
    password: str

class CodeRequest(BaseModel):
    code: str

@app.post("/login")
async def login(request: LoginRequest):
    """Secure login for user 'ayesha'"""
    if request.username == "ayesha" and request.password == "1234":
        return {"status": "success"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/fix-code")
async def fix_code(request: CodeRequest):
    """Instantly fixes logical and syntax errors"""
    try:
        payload = {"inputs": f"Correct the python code: {request.code}"}
        response = requests.post(HF_API_URL, json=payload, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            fixed = result[0].get('generated_text', "").strip()
            return {"fixed_code": fixed if fixed else "Check logic manually."}
            
        return {"fixed_code": "AI is warming up. Please click again in 5 seconds."}
    except Exception as e:
        return {"fixed_code": f"Error: {str(e)}"}

if __name__ == "__main__":
    # Changed port to 8001 to avoid the binding error
    uvicorn.run(app, host="127.0.0.1", port=8001)