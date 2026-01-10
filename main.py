from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pyodbc

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-EGH82B2;"
        "DATABASE=CodeErrorHelperDB;"
        "Trusted_Connection=yes;"
    )

class ErrorEntry(BaseModel):
    title: str
    description: str

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(user: LoginRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT id, username, full_name FROM Users WHERE username = ? AND password = ?"
    cursor.execute(query, (user.username, user.password))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"status": "success", "user": {"id": row[0], "username": row[1], "name": row[2]}}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/errors/")
def get_errors():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Screenshot ke mutabiq 'title' column use kiya hai
    cursor.execute("SELECT id, title, description FROM errors")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "description": r[2]} for r in rows]

@app.post("/errors/")
def add_error(error: ErrorEntry):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO errors (title, description) VALUES (?, ?)", (error.title, error.description))
    conn.commit()
    conn.close()
    return {"message": "Success"}