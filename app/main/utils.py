import re
from datetime import datetime
from app.config import TRUSTED_SITES

def parse_term_and_source(user_input):
    """
    Extracts the main query term and an optional source (like aws, gcp, finops) from the user's input.

    Returns:
        term (str): The cleaned query term.
        source (str or None): The detected source keyword (e.g. "aws") if found.
    """
    user_input_lower = user_input.lower()
    source = None

    # Try to match known trusted sources using patterns
    for key in TRUSTED_SITES.keys():
        patterns = [
            rf"\baccording to {key}\b",
            rf"\bon {key}\b",
            rf"\bin {key}\b",
            rf"^{key}\b",        # e.g. "aws savings"
            rf"\b{key}\b"        # any position
        ]
        for pat in patterns:
            if re.search(pat, user_input_lower):
                source = key
                break
        if source:
            break

    # Remove matched phrases from input
    if source:
        cleaned = re.sub(rf"\b(according to|on|in)?\s*{source}\b", "", user_input_lower, flags=re.IGNORECASE).strip()
    else:
        cleaned = user_input_lower

    # Remove polite/questional wrappers
    cleaned = re.sub(
        r"^(what is|what's|explain|define|tell me about|give me info on|can you explain|please explain|please define)\s+",
        "",
        cleaned
    )
    cleaned = re.sub(r"[?\.]", "", cleaned).strip()

    # Fallback to original input if cleaned is empty
    term = cleaned if cleaned else user_input_lower.strip()

    return term, source

def log_interaction(user_email, user_input, response, log_file="chat_logs.txt"):
    """
    Logs a chatbot interaction to a local text file.

    Args:
        user_email (str): Email of the user who sent the message.
        user_input (str): The raw message from the user.
        response (str): The bot's response.
        log_file (str): Path to the log file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {user_email}\n")
        f.write(f"User: {user_input}\n")
        f.write(f"Bot: {response}\n")
        f.write("-" * 40 + "\n")
