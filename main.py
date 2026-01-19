from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn

app = FastAPI()

# 1. CORS Middleware for frontend-backend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Stable Hugging Face Model
HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/phi-2"

class LoginRequest(BaseModel):
    username: str
    password: str

class CodeRequest(BaseModel):
    code: str

# 3. Login Route
@app.post("/login")
async def login(request: LoginRequest):
    """Verifies credentials for user 'ayesha'"""
    if request.username == "ayesha" and request.password == "1234":
        return {"status": "success"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# 4. Refined AI Fix-Code Route
@app.post("/fix-code")
async def fix_code(request: CodeRequest):
    """Refined logic to catch syntax and logical errors"""
    try:
        # Instruction for the AI to be more strict
        instruction = (
            f"Context: You are a Python expert. Fix syntax and logic in this code.\n"
            f"Input: {request.code}\n"
            f"Fixed Code:"
        )
        
        # English: Sending the request with parameters
        payload = {"inputs": instruction, "parameters": {"return_full_text": False}}
        response = requests.post(HF_API_URL, json=payload, timeout=60)
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            fixed = result[0].get('generated_text', "").strip()
            
            # Handling empty or unchanged responses
            if not fixed or fixed == request.code:
                return {"fixed_code": "No errors found, but check your logic again!"}
                
            return {"fixed_code": fixed}
            
        return {"fixed_code": "AI server is busy, try again in 5 seconds."}
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"fixed_code": "Connection error with AI."}

# 5. Server Configuration
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)