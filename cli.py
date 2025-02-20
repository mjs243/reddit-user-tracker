import requests
import argparse

BASE_URL = "http://127.0.0.1:8000"

def track(username, user):
    url = f"{BASE_URL}/track/{username}"
    headers = {"X-Reddit-Username": user}
    response = requests.post(url, headers=headers)
    print(response.json())

def untrack(username, user):
    url = f"{BASE_URL}/untrack/{username}"
    headers = {"X-Reddit-Username": user}
    response = requests.delete(url, headers=headers)
    print(response.json())

def main():
    parser = argparse.ArgumentParser(description="CLI for Reddit Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # Track user
    track_parser = subparsers.add_parser("track", help="Track a Reddit user")
    track_parser.add_argument("username", help="Reddit username to track")
    track_parser.add_argument("--user", required=True, help="Your Reddit username (for auth)")

    # Untrack user
    untrack_parser = subparsers.add_parser("untrack", help="Untrack a Reddit user")
    untrack_parser.add_argument("username", help="Reddit username to untrack")
    untrack_parser.add_argument("--user", required=True, help="Your Reddit username (for auth)")

    args = parser.parse_args()

    if args.command == "track":
        track(args.username, args.user)
    elif args.command == "untrack":
        untrack(args.username, args.user)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
