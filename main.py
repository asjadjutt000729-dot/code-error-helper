from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# New Smart Model for Logic: Salesforce CodeT5
HF_API_URL = "https://api-inference.huggingface.co/models/Salesforce/codet5-large"

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
    """Advanced logical and syntax error detection"""
    try:
        # Instruction for the expert model
        payload = {"inputs": f"Fix syntax and logic in this Python code: {request.code}"}
        response = requests.post(HF_API_URL, json=payload, timeout=60)
        
        # Check for model loading status
        if response.status_code == 503:
            return {"fixed_code": "AI is warming up. Wait 10s and click again."}
            
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            fixed = result[0].get('generated_text', "").strip()
            
            # Logic to ensure we don't return an empty box
            if not fixed or fixed == request.code:
                return {"fixed_code": "Your logic looks fine, but double check your operators!"}
                
            return {"fixed_code": fixed}
            
        return {"fixed_code": "AI is busy, please retry in 5 seconds."}
        
    except Exception as e:
        print(f"Server Error: {str(e)}")
        return {"fixed_code": "Connection issue. Check your internet."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)