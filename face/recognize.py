import cv2
import numpy as np
from deepface import DeepFace


def get_face_embedding(frame):
    """
    Generate a normalized face embedding from a BGR frame.
    Returns a list (embedding) or None if the face cannot be processed.
    """
    if frame is None:
        print("[FACE] Received None frame.")
        return None

    if not isinstance(frame, np.ndarray) or frame.size == 0:
        print("[FACE] Invalid or empty frame.")
        return None

    try:
        result = DeepFace.represent(
            img_path=frame,
            model_name="Facenet512",
            enforce_detection=False,
            detector_backend="opencv"
        )

        if not result or len(result) == 0:
            return None

        emb = result[0]["embedding"]
        emb = np.array(emb, dtype=np.float32)
        norm = np.linalg.norm(emb)

        if norm == 0:
            print("[FACE] Zero-norm embedding, skipping.")
            return None

        return (emb / norm).tolist()

    except Exception as e:
        print(f"[FACE] Embedding error: {e}")
        return None