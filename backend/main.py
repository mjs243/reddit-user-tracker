from fastapi import FastAPI, Depends, HTTPException, Request
import requests
import sqlite3
import os
from urllib.parse import urlencode
from backend.database import init_db

app = FastAPI()

init_db()

# Reddit OAuth Credentials
CLIENT_ID = "1Jfn8k53QIE6afiBbcNQqA"
CLIENT_SECRET = "4kWU3zdJfDwzPXHhnCBQlNP0YPQczA"
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

# Step 0: Default Homepage
@app.get("/")
def home():
    return {"message": "Reddit User Tracker API is running!"}

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
    
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    auth = (CLIENT_ID, CLIENT_SECRET)

    response = requests.post(TOKEN_URL, data=data, auth=auth, headers={"User-Agent": "RedditTracker/1.0"})
    token_data = response.json()

    if "access_token" not in token_data:
        raise HTTPException(status_code=400, detail="Failed to retrieve access token")

    access_token = token_data["access_token"]
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data["expires_in"]

    # Fetch Reddit username
    user_info = requests.get("https://oauth.reddit.com/api/v1/me", headers={
        "Authorization": f"bearer {access_token}",
        "User-Agent": "RedditTracker/1.0"
    }).json()

    reddit_username = user_info["name"]

    # Store user in database
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO users (reddit_username, access_token, refresh_token, token_expires) VALUES (?, ?, ?, ?)",
        (reddit_username, access_token, refresh_token, expires_in))
        conn.commit()

    return {"message": "Login successful!", "user": reddit_username}

# Step 3: Track Users
@app.post("/track/{username}")
def track_user(username: str, request: Request):
    user = request.headers.get("X-Reddit-Username")
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO tracked_users (owner, reddit_username) VALUES (?, ?)", (user, username))
        conn.commit()

    return {"message": f"Now tracking {username}"}

# Step 4: Delete Tracked Users
@app.delete("/untrack/{username}")
def untrack_user(username: str, request: Request):
    user = request.headers.get("X-Reddit-Username")
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tracked_users WHERE owner=? AND reddit_username=?", (user, username))
        conn.commit()

    return {"message": f"Stopped tracking {username}"}