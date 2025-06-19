import os
import json
import hashlib
import joblib
from sklearn.pipeline import Pipeline

MODEL_PATH = "intent_classifier.joblib"
TRAINING_DATA_PATH = "training_data.json"
HASH_FILE = "intent_hash.txt"

def _get_data_hash():
    with open(TRAINING_DATA_PATH, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def _needs_retraining():
    current_hash = _get_data_hash()
    if not os.path.exists(HASH_FILE) or not os.path.exists(MODEL_PATH):
        return True
    with open(HASH_FILE, "r") as f:
        stored_hash = f.read().strip()
    return stored_hash != current_hash

def _save_hash():
    with open(HASH_FILE, "w") as f:
        f.write(_get_data_hash())

def train_if_needed():
    if not _needs_retraining():
        return

    from app.intent.train_intent_classifier import train_intent_model
    train_intent_model()
    _save_hash()
