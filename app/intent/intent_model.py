import os
import json
import hashlib
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from app.config import MODEL_PATH, TRAINING_DATA_PATH, HASH_FILE

_model = None  # Global model instance

def _get_data_hash():
    with open(TRAINING_DATA_PATH, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def _needs_retraining():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(HASH_FILE):
        return True
    with open(HASH_FILE, "r") as f:
        return f.read().strip() != _get_data_hash()

def _save_hash():
    with open(HASH_FILE, "w") as f:
        f.write(_get_data_hash())

def _train_model():
    from app.intent.train_intent_classifier import train_intent_model
    train_intent_model()
    _save_hash()

def _load_model():
    global _model
    _model = joblib.load(MODEL_PATH)

def classify_intent(text):
    global _model
    if _needs_retraining():
        _train_model()
    if _model is None:
        _load_model()
    return _model.predict([text])[0]
