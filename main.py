from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn

app = FastAPI()

# Enable CORS to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# New Faster Hugging Face Model for Code Repair
HF_API_URL = "https://api-inference.huggingface.co/models/Salesforce/codet5-large"

class LoginRequest(BaseModel):
    username: str
    password: str

class CodeRequest(BaseModel):
    code: str

@app.post("/login")
async def login(request: LoginRequest):
    """Simple login check for Ayesha"""
    if request.username == "ayesha" and request.password == "1234":
        return {"status": "success"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/fix-code")
async def fix_code(request: CodeRequest):
    """Processes code fixing using Hugging Face Free API"""
    try:
        # English: Preparing the request payload
        payload = {"inputs": f"Fix python: {request.code}"}
        response = requests.post(HF_API_URL, json=payload)
        
        if response.status_code != 200:
             # Handle model loading or busy state
             raise Exception("AI model is initializing, please wait.")

        result = response.json()
        fixed = result[0]['generated_text'] if isinstance(result, list) else "Processing error"
        return {"fixed_code": fixed}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)