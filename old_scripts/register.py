# register.py

import json
import os
import hashlib
from app.auth.email_verification import send_verification_email
from app.config import USERS_FILE


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user():
    users = load_users()

    full_name = input("Full name: ").strip()
    email = input("Company email: ").strip().lower()
    employee_id = input("Employee ID: ").strip()
    receiver_email = email

    if email in users:
        print(" Email already registered.")
        return None, None

    password = input("Choose a password: ").strip()

    verification_code = send_verification_email(email)
    if not verification_code:
        print("Could not send verification email. Try again later.")
        return None, None

    entered_code = input("Enter the verification code sent to your email: ").strip()
    if entered_code != verification_code:
        print(" Verification failed.")
        return None, None

    users[email] = {
        "full_name": full_name,
        "password": hash_password(password),
        "employee_id": employee_id,
        "role": "user",  # Default role
    }

    save_users(users)
    print("Registration successful.")
    return email, "user"
