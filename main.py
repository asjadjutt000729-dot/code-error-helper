from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Using Salesforce CodeT5 for deep logical analysis
HF_API_URL = "https://api-inference.huggingface.co/models/Salesforce/codet5-large"

class CodeRequest(BaseModel):
    code: str

@app.post("/fix-code")
async def fix_code(request: CodeRequest):
    """Deep logic repair for Python"""
    try:
        # English: Direct instruction for syntax and logic
        payload = {"inputs": f"Fix syntax and logical errors in this Python code: {request.code}"}
        response = requests.post(HF_API_URL, json=payload, timeout=60)
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            fixed = result[0].get('generated_text', "").strip()
            
            if not fixed or fixed == request.code:
                return {"fixed_code": "No logical errors found. Double check your input!"}
                
            return {"fixed_code": fixed}
        
        # Handling busy state
        return {"fixed_code": "AI is warming up. Please click 'Fix My Code' again in 10 seconds."}
        
    except Exception as e:
        return {"fixed_code": f"Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)