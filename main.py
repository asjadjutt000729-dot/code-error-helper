import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles #
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Configure Gemini AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash") #

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the frontend folder to serve HTML files
# Make sure your folder name is exactly 'frontend'
app.mount("/static", StaticFiles(directory="frontend"), name="static")

class CodeRequest(BaseModel):
    code: str

@app.post("/fix-code")
async def fix_code(request: CodeRequest):
    try:
        # Prompt for Gemini AI
        prompt = f"Fix the following Python code and explain the errors briefly in English:\n\n{request.code}"
        
        response = model.generate_content(prompt)
        
        if not response.text:
            raise HTTPException(status_code=500, detail="AI returned an empty response")
            
        return {"fixed_code": response.text}
    
    except Exception as e:
        # Handling errors like the 500 error seen in logs
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Server is running! Go to /static/index.html"}