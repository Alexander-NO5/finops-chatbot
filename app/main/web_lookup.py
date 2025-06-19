import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from app.config import CRAWLED_DATA_FILE, FAISS_INDEX_FILE, EMBEDDINGS_FILE, SEMANTIC_MODEL_NAME
from core.cache_manager import get_cached_result, set_cached_result

model = SentenceTransformer(SEMANTIC_MODEL_NAME)

# Lazy-load on first use
index = None
documents = None

def build_index():
    global index, documents
    if not os.path.exists(CRAWLED_DATA_FILE):
        raise FileNotFoundError("Crawled data not found.")

    with open(CRAWLED_DATA_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)

    texts = [doc["title"] + " " + doc["text"] for doc in documents]
    embeddings = model.encode(texts, convert_to_numpy=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    np.save(EMBEDDINGS_FILE, embeddings)
    faiss.write_index(index, FAISS_INDEX_FILE)

def load_index():
    global index, documents
    if not os.path.exists(FAISS_INDEX_FILE) or not os.path.exists(EMBEDDINGS_FILE):
        build_index()

    index = faiss.read_index(FAISS_INDEX_FILE)

    with open(CRAWLED_DATA_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)

def semantic_search(query, top_k=3):
    global index, documents
    if index is None or documents is None:
        load_index()

    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        doc = documents[idx]
        snippet = doc['text'][:300] + "..." if len(doc['text']) > 300 else doc['text']
        results.append(
            f"<strong>{doc['title']}</strong><br>{snippet}<br><a href='{doc['url']}' target='_blank'>{doc['url']}</a>"
        )
    return "<br><br>".join(results)

def semantic_search_cached(query, top_k=3):
    cache_key = f"semantic::{query.lower().strip()}"
    cached = get_cached_result(cache_key)
    if cached:
        return cached

    result = semantic_search(query, top_k)
    set_cached_result(cache_key, result)
    return result
