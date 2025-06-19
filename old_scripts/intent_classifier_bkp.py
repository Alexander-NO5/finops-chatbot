import re

def classify_intent(user_input):
    text = user_input.lower().strip()

    # Expanded intent phrases
    greetings = [
        "hi", "hello", "hey", "good morning", "good afternoon", "good evening", "hiya", "howdy",
        "hey there", "hi there", "yo", "sup", "greetings", "what's up", "how's it going"
    ]

    farewells = [
        "bye", "goodbye", "see you", "take care", "later", "farewell", "see ya", "catch you later",
        "peace out", "adios", "ciao", "talk to you later"
    ]

    gratitude = [
        "thanks", "thank you", "cheers", "much appreciated", "thank you very much",
        "thanks a lot", "many thanks", "appreciate it", "grateful", "thank you kindly"
    ]

    question_patterns = [
        r"\bwhat is\b", r"\bhow (do|does|can)\b", r"\bwhy\b", r"\bwho\b", r"\bwhen\b", r"\bexplain\b", r"\bdefine\b",
        r"\bwhat are\b", r"\bcan you\b", r"\bcould you\b", r"\bis it\b", r"\bare there\b", r"\bdoes it\b", r"\?\s*$"
    ]

    command_prefixes = ["help:", "list:", "show:", "teach:", "update:", "alias:", "delete:"]

    web_lookup_phrases = [
        "according to aws", "according to gcp", "according to finops",
        "on aws", "in aws", "on gcp", "in gcp", "on finops", "in finops foundation"
    ]

    # === Classification logic ===
    if any(text.startswith(cmd) for cmd in command_prefixes):
        return "command"

    if any(word in text for word in greetings):
        return "greeting"

    if any(word in text for word in farewells):
        return "farewell"

    if any(word in text for word in gratitude):
        return "gratitude"

    if any(re.search(pattern, text) for pattern in question_patterns):
        return "question"

    if any(phrase in text for phrase in web_lookup_phrases):
        return "web_lookup"

    if len(text.split()) <= 3 and any(w in text for w in greetings + farewells + gratitude):
        return "smalltalk"

    return "unknown"
