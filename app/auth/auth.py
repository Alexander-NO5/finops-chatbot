import json
import hashlib
import os
from app.auth.email_verification import send_verification_email
from app.config import USERS_FILE

# Load users from JSON file
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

# Save users to JSON file
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Hash password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register a new user
def register_user(full_name, email, password, employee_id):
    users = load_users()
    email = email.lower()

    if email in users:
        return "Email already registered."

    users[email] = {
        "full_name": full_name,
        "password": hash_password(password),
        "employee_id": employee_id,
        "role": "user",
        "verified": False
    }

    save_users(users)
    send_verification_email(full_name, email)
    return "Registration successful. Please check your email to verify your account."

# Authenticate user (checks hashed password and verification)
def authenticate_user(email, password):
    users = load_users()
    email = email.lower()

    if email in users:
        hashed_input = hash_password(password)
        if users[email]["password"] == hashed_input and users[email].get("verified", False):
            return users[email]  # Return user object
    return None

def reset_password(email, new_password):
    users = load_users()
    if email in users:
        users[email]["password"] = hash_password(new_password)
        save_users(users)
        return True
    return False

# Check if user is admin
def is_admin(email):
    """
    Returns True if the user has an 'admin' role.
    """
    users = load_users()
    user = users.get(email.lower())
    return user and user.get("role", "").lower() == "admin"

# Mark user as verified
def mark_user_as_verified(email):
    try:
        users = load_users()
        email = email.lower()

        if email in users:
            users[email]["verified"] = True
            save_users(users)
            return True
        return False
    except Exception as e:
        print(f"Error verifying user: {e}")
        return False

# Retrieve user object by email
def get_user_by_email(email):
    users = load_users()
    return users.get(email.lower())
