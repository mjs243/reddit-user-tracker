import sqlite3

DB_FILE = "users.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        # Ensure the users table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reddit_username TEXT UNIQUE,
                access_token TEXT,
                refresh_token TEXT,
                token_expires INTEGER
            )
        """)

        # Table to store tracked users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracked_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner TEXT,
                reddit_username TEXT UNIQUE
            )
        """)
        
        conn.commit()

init_db()