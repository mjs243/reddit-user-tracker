from fastapi import FastAPI, Depends, HTTPException, Request
import requests
import sqlite3
import os
from urllib.parse import urlencode

app = FastAPI()

# Reddit OAuth Credentials
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
REDIRECT_URI = "http://localhost:8000/auth/callback"
API_BASE = "https://www.reddit.com/api/v1"
AUTH_URL = f"{API_BASE}/authorize"
TOKEN_URL = f"{API_BASE}/access_token"

# Database Setup
DB_FILE = "users.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
           CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reddit_username TEXT UNIQUE,
                access_token TEXT,
                refresh_token TEXT,
                token_expires INTEGER           
            )            
        """)
        conn.commit()

init_db()

# Step 1: Redirect user to Reddit for authenticaiton
@app.get("/auth/login")
def login():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "state": "random_state_string",
        "redirect_uri": REDIRECT_URI,
        "duration": "permanent",
        "scope": "identity read"
    }
    return {"url": f"{AUTH_URL}?{urlencode(params)}"}

# Step 2: Handle OAuth callback
@app.get("/auth/callback")
def auth_callback(code: str, state: str):
    if state != "random_state_string":
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    