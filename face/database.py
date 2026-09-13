import chromadb
import numpy as np
import os
import base64

FACE_DB_DIR = "data/face_db"
FACE_PHOTOS_DIR = "data/face_photos"  # NEW: folder to store profile photos
_client = None
_collection = None

os.makedirs(FACE_PHOTOS_DIR, exist_ok=True)


def get_face_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=FACE_DB_DIR)
        _collection = _client.get_or_create_collection(
            name="campus_faces",
            metadata={"hnsw:space": "cosine"}
        )
    return _collection


def save_face(person_id: str, embedding: list, metadata: dict):
    collection = get_face_collection()
    collection.upsert(
        ids=[person_id],
        embeddings=[embedding],
        metadatas=[metadata]
    )
    print(f"Face saved for: {metadata.get('name')}")


def save_face_photo(person_id: str, frame) -> str:
    """
    Save a captured frame as a profile photo jpg.
    Returns the saved photo path.
    """
    import cv2
    photo_path = os.path.join(FACE_PHOTOS_DIR, f"{person_id}.jpg")
    cv2.imwrite(photo_path, frame)
    print(f"Profile photo saved: {photo_path}")
    return photo_path


def get_face_photo_base64(person_id: str) -> str:
    """
    Read the saved profile photo and return as base64 string
    so it can be sent over WebSocket and displayed in the browser.
    Returns None if photo doesn't exist.
    """
    photo_path = os.path.join(FACE_PHOTOS_DIR, f"{person_id}.jpg")
    if not os.path.exists(photo_path):
        return None
    with open(photo_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"


def find_closest_face(embedding: list, top_k: int = 1):
    collection = get_face_collection()
    if collection.count() == 0:
        return None, None
    results = collection.query(
        query_embeddings=[embedding],
        n_results=min(top_k, collection.count())
    )
    if not results["ids"][0]:
        return None, None
    return results["metadatas"][0][0], results["distances"][0][0]


def get_all_faces():
    return get_face_collection().get(include=["metadatas", "embeddings"])


def face_count():
    return get_face_collection().count()