import chromadb
import numpy as np
import os

FACE_DB_DIR = "data/face_db"
_client = None
_collection = None

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
    print(f"✅ Face saved for: {metadata.get('name')}")

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