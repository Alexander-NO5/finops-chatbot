import json
import os
import inflect
from app.config import KNOWLEDGE_FILE

# Initialize inflect engine for singularizing words
p = inflect.engine()

def load_knowledge():
    """
    Load the knowledge base from a JSON file.
    Returns an empty dictionary if the file does not exist.
    """
    if not os.path.exists(KNOWLEDGE_FILE):
        return {}
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_knowledge(knowledge, filepath=KNOWLEDGE_FILE):
    """
    Save the current knowledge base to a JSON file.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(knowledge, f, indent=4)

def normalize(text):
    """
    Normalize a term for consistent lookup:
    - Strip whitespace
    - Convert to lowercase
    - Convert plurals to singular form
    """
    term = text.strip().lower()
    singular = p.singular_noun(term)
    return singular if singular else term

def resolve(term, knowledge, max_depth=5):
    """
    Resolve an alias term to its original term by following alias chains.
    Stops after max_depth to prevent infinite loops.
    """
    term = term.strip().lower()
    depth = 0

    while depth < max_depth:
        value = knowledge.get(term, "")
        if isinstance(value, str) and value.startswith("__alias__"):
            term = value.replace("__alias__:", "").strip()
            depth += 1
        else:
            break

    return term
