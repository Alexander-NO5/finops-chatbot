import json
import os

USERS_FILE = "users.json"

def login_user():
    print("\nLogin")

    email = input("Email: ").strip()
    password = input("Password: ").strip()

    if not os.path.exists(USERS_FILE):
        print("No registered users found.")
        return None

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    if email in users:
        user = users[email]
        if user["password"] == password:
            print(f"Welcome back, {user['full_name']}!")
            return {
                "email": email,
                "role": user["role"]
            }

    print("Invalid email or password.")
    return None
