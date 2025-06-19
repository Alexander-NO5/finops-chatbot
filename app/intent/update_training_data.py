import json
import os
from app.config import KNOWLEDGE_FILE, TRAINING_DATA_PATH, STATIC_DATA_FILE

def update_training_data_from_knowledge():
    with open(KNOWLEDGE_FILE, "r") as f:
        knowledge = json.load(f)

    # Load static training data
    if not os.path.exists(STATIC_DATA_FILE):
        raise FileNotFoundError("original_training_data.json not found.")
    with open(STATIC_DATA_FILE, "r") as f:
        training_data = json.load(f)

    # Remove old dynamic knowledge examples
    training_data = [item for item in training_data if item.get("intent") != "dynamic_knowledge"]

    # Extract non-alias terms as training examples
    new_questions = [
        term for term, value in knowledge.items()
        if not (isinstance(value, str) and value.startswith("__alias__:"))
    ]
    if new_questions:
        training_data.append({
            "intent": "dynamic_knowledge",
            "examples": new_questions
        })

    # Save new training data
    with open(TRAINING_DATA_PATH, "w") as f:
        json.dump(training_data, f, indent=2)
