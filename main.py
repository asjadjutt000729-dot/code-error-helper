import os
# Importing the new library to fix the FutureWarning
from google import genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration using the new GenAI client
# Use your K94o key from Jan 18, 2026
client = genai.Client(api_key="AIzaSyBzYiRDiLdhxR2YkeTMLN3JhMMbClHK94o")

class CodeRequest(BaseModel):
    code: str

@app.post("/fix-code")
async def fix_code(request: CodeRequest):
    """Sends code to AI and returns the fixed version"""
    try:
        # Prompting the model for a clean fix
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=f"Fix this Python code. Return ONLY the corrected code:\n\n{request.code}"
        )
        return {"fixed_code": response.text}
    except Exception as e:
        # Logs specific error for debugging
        print(f"AI Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Make sure no other terminal is using port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)