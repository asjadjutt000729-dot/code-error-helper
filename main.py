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

# Hugging Face Public API URL (No Key required for basic testing)
HF_API_URL = "https://api-inference.huggingface.co/models/Salesforce/codet5-base"

class LoginRequest(BaseModel):
    username: str
    password: str

class CodeRequest(BaseModel):
    code: str

@app.post("/login")
async def login(request: LoginRequest):
    """Simple login for Ayesha"""
    if request.username == "ayesha" and request.password == "1234":
        return {"status": "success"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/fix-code")
async def fix_code(request: CodeRequest):
    """Uses Hugging Face Free AI to fix Python code"""
    try:
        # English comment: Sending request to Hugging Face model
        payload = {"inputs": f"Repair this python code: {request.code}"}
        response = requests.post(HF_API_URL, json=payload)
        
        if response.status_code != 200:
            raise Exception("AI is currently busy or loading")

        result = response.json()
        
        # Extracting fixed code from response
        fixed = result[0]['generated_text'] if isinstance(result, list) else "Error in AI processing"
        return {"fixed_code": fixed}
    except Exception as e:
        print(f"Detailed Error: {str(e)}")
        raise HTTPException(status_code=500, detail="AI Service Temporarily Offline")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)