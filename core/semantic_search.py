import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

# Load the same model used for encoding (must match crawler/indexing phase)
MODEL_NAME = "all-MiniLM-L6-v2" 
model = SentenceTransformer(MODEL_NAME)

# Paths to index + metadata
FAISS_INDEX_PATH = "semantic_index/faiss.index"
DOCS_METADATA_PATH = "semantic_index/docs.json"

# Load index and metadata
def load_index():
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(DOCS_METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata

index, metadata = load_index()


def query_semantic_knowledge(query, top_k=3):
    """
    Perform a semantic search over pre-embedded docs.
    Returns a list of dicts: [{title, snippet, url}]
    """
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), top_k)

    results = []
    for idx in I[0]:
        if 0 <= idx < len(metadata):
            doc = metadata[idx]
            results.append({
                "title": doc.get("title", "Result"),
                "snippet": doc.get("text", "")[:300],
                "url": doc.get("url", "")
            })
    return results
