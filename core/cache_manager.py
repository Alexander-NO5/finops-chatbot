import json
import time
import os
import atexit

# Constants
CACHE_FILE = "cache.json"
CACHE_TTL = 48 * 3600  # 48 hours in seconds

# Internal module-level cache and state tracking
_cache = None  # Holds the loaded cache in memory
_cache_dirty = False  # Tracks if the cache has been modified and needs saving

def load_cache():
    """Load the cache from disk if not already loaded."""
    global _cache
    if _cache is not None:
        return _cache
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                loaded_cache = json.load(f)
            # Ensure timestamp is float
            for key in loaded_cache:
                loaded_cache[key]["timestamp"] = float(loaded_cache[key]["timestamp"])
            _cache = loaded_cache
            return _cache
        except Exception:
            pass
    _cache = {}
    return _cache

def save_cache():
    """Write the current in-memory cache to disk if it was modified."""
    global _cache_dirty
    if not _cache_dirty:
        return
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            cache_to_save = {
                key: {
                    "result": value["result"],
                    "timestamp": str(value["timestamp"])
                } for key, value in _cache.items()
            }
            json.dump(cache_to_save, f, indent=2)
        _cache_dirty = False
    except Exception as e:
        print(f"Warning: Failed to save cache file: {e}")

def get_cached_result(key):
    """Retrieve a result from cache if it's still valid."""
    global _cache_dirty
    cache = load_cache()
    entry = cache.get(key)
    if entry:
        if time.time() - entry["timestamp"] < CACHE_TTL:
            return entry["result"]
        else:
            # Remove expired cache entry
            del cache[key]
            _cache_dirty = True
    return None

def set_cached_result(key, result):
    """Add or update a cached result and mark it dirty."""
    global _cache_dirty
    cache = load_cache()
    cache[key] = {
        "result": result,
        "timestamp": time.time()
    }
    _cache_dirty = True

# Automatically save cache on app exit
atexit.register(save_cache)
