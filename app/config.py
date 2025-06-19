# config.py
import os

# === App & Security ===
SECRET_KEY = "2302256298e328d280ab46af5aa1d37715d98f4fbb0d824ae6d105c9889b2cf8"

# === Email settings ===
SENDER_EMAIL = "finopsbot@gmail.com"
SENDER_PASSWORD = "asqz jtmk vggp vbop"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# === Trusted sites ===
TRUSTED_SITES = {
    "aws": "aws.amazon.com",
    "gcp": "cloud.google.com",
    "finops": "finopsfoundation.org"
}

# === Base directory for data files ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

# === File paths ===
USERS_FILE = os.path.join(BASE_DIR, "users.json")
KNOWLEDGE_FILE = os.path.join(BASE_DIR, "knowledge.json")
MODEL_PATH = os.path.join(BASE_DIR, "intent_classifier.joblib")
TRAINING_DATA_PATH = os.path.join(BASE_DIR, "training_data.json")
HASH_FILE = os.path.join(BASE_DIR, "intent_hash.txt")
STATIC_DATA_FILE = os.path.join(BASE_DIR, "original_training_data.json")
SEARCH_QUOTA_FILE = os.path.join(BASE_DIR, "web_quota.json")

# === Semantic Search Settings ===
CRAWLED_DATA_FILE = os.path.join(BASE_DIR, "crawled_data.json")
FAISS_INDEX_FILE = os.path.join(BASE_DIR, "semantic_index.faiss")
EMBEDDINGS_FILE = os.path.join(BASE_DIR, "doc_embeddings.npy")

SEMANTIC_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"