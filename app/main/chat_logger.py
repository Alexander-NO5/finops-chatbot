import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_chat(user_email, question, answer):
    """Log a single chat entry to a user-specific daily file."""
    email = user_email if user_email else "anonymous"

    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%H:%M:%S")

    user_folder = os.path.join(LOG_DIR, email)
    os.makedirs(user_folder, exist_ok=True)

    log_file = os.path.join(user_folder, f"{today}.txt")

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] Q: {question.strip()}\n")
            f.write(f"[{timestamp}] A: {answer.strip()}\n\n")
    except Exception as e:
        print(f"Error writing chat log: {e}")
