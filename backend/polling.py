import requests
import sqlite3
import time

DB_FILE = "users.db"

def get_access_token(owner):
    """Retrieve the stored access token for the user"""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT access_token FROM users WHERE reddit_username = ?", (owner,))
        result = cursor.fetchone()
        return result[0] if result else None

def get_new_posts(username, access_token):
    """Fetch the latest posts from a user"""
    url = f"https://oauth.reddit.com/user/{username}/submitted"
    headers = {"Authorization": f"bearer {access_token}", "User-Agent": "RedditTracker/1.0"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]["children"]
    return []

def poll_users():
    """Poll all tracked users for new posts"""
    while True:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT owner, reddit_username FROM tracked_users")
            tracked_users = cursor.fetchall()

        for owner, username in tracked_users:
            access_token = get_access_token(owner)
            if not access_token:
                print(f"Skipping {username}, no token available.")
                continue
            new_posts = get_new_posts(username, access_token)
            if new_posts:
                latest_post = new_posts[0]["data"]["title"]
                print(f"New post from {username}: {latest_post}")

        time.sleep(10)

if __name__ == "__main__":
    poll_users()