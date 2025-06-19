import hashlib
from pathlib import Path
from app.intent.update_training_data import update_training_data_from_knowledge
from app.config import MODEL_PATH, TRAINING_DATA_PATH, HASH_FILE

def _get_data_hash():
    training_path = Path(TRAINING_DATA_PATH)
    if not training_path.exists():
        return ""
    return hashlib.md5(training_path.read_bytes()).hexdigest()

def _needs_retraining(force=False):
    if force:
        print("[Intent] Force retraining requested.")
        return True

    current_hash = _get_data_hash()

    if not Path(HASH_FILE).exists() or not Path(MODEL_PATH).exists():
        print("[Intent] Missing hash or model file. Retraining required.")
        return True

    stored_hash = Path(HASH_FILE).read_text().strip()
    needs = stored_hash != current_hash
    if needs:
        print("[Intent] Detected change in training data. Retraining needed.")
    return needs

def _save_hash():
    Path(HASH_FILE).write_text(_get_data_hash())

def train_if_needed(force=False):
    if not _needs_retraining(force):
        print("[Intent] Model is up to date. No retraining needed.")
        return
    try:
        update_training_data_from_knowledge()  # <-- THIS
        from app.intent.train_intent_classifier import train_intent_model
        print("[Intent] Retraining intent classifier...")
        train_intent_model()
        _save_hash()
        print("[Intent] Retraining complete.")
    except Exception as e:
        print(f"[Intent] ERROR during retraining: {e}")
