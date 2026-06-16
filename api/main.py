import os
import socket

def _check_online():
    try:
        socket.setdefaulttimeout(1.0)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except OSError:
        return False

_HF_CACHE = os.path.expanduser("~/.cache/huggingface/hub")
_MODEL_CACHED = os.path.exists(_HF_CACHE) and any(
    "MiniLM" in d for d in os.listdir(_HF_CACHE)
) if os.path.exists(_HF_CACHE) else False

if _MODEL_CACHED and not _check_online():
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    print("[STARTUP] Offline mode — using cached models.")
import sys
import re
import uuid
import threading
import asyncio
import queue
import numpy as np
import cv2

os.environ["PATH"] += os.pathsep + r"C:\Users\dkk82\AppData\Local\Microsoft\WinGet\Links"

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.query import load_rag_chain, ask
from face.database import save_face, find_closest_face, face_count
from api.tts import speak, stop_speech
from api.stt import listen_once, listen_wake_word

FACE_ENABLED = True
DeepFace = None

try:
    from face.recognize import get_face_embedding
    from deepface import DeepFace
except Exception as e:
    print(f"[FACE] Disabled: {e}")
    FACE_ENABLED = False

    def get_face_embedding(frame):
        return None

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UI_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ui", "build")
if os.path.exists(UI_DIR):
    app.mount("/static", StaticFiles(directory=os.path.join(UI_DIR, "static")), name="static")

_rag_chain = None
VERIFY_THRESHOLD = 0.30
_mic_lock = asyncio.Lock()
_wake_queue = queue.Queue()

# FIX: flag to pause wake word loop during registration or active session
_is_registering = False
_session_active = False

EXIT_PHRASES = ["bye", "goodbye", "exit", "quit", "that's all", "ok bye",
                "thank you bye", "see you", "close", "end session"]


def clean(text):
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"#+\s*", "", text)
    text = re.sub(r"\n+", ". ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_for_tts(text: str) -> str:
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_chain():
    global _rag_chain
    if _rag_chain is None:
        _rag_chain = load_rag_chain()
    return _rag_chain


def _wake_word_loop():
    """Wake word listener — pauses during active sessions and registration."""
    while True:
        try:
            # FIX: don't listen for wake word during active session or registration
            if _session_active or _is_registering:
                import time
                time.sleep(0.5)
                continue

            detected = listen_wake_word(timeout=4)
            if detected and _wake_queue.qsize() == 0:
                _wake_queue.put(True)
        except Exception as e:
            print(f"[WAKE LOOP] Error: {e}")


def open_camera():
    """
    Open camera with DirectShow backend on Windows to avoid MSMF WARN errors.
    Falls back to default if CAP_DSHOW is not available.
    """
    try:
        # FIX: use CAP_DSHOW on Windows to avoid cap_msmf.cpp async errors
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            # fallback
            cap.release()
            cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            cap.release()
            print("[CAMERA] Camera not found or already in use.")
            return None
        # FIX: set stable resolution and framerate
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 15)
        return cap
    except Exception as e:
        print(f"[CAMERA] Failed to open camera: {e}")
        return None


@app.on_event("startup")
async def startup():
    threading.Thread(target=get_chain, daemon=True).start()
    threading.Thread(target=_wake_word_loop, daemon=True).start()


@app.get("/")
async def root():
    index = os.path.join(UI_DIR, "index.html")
    if os.path.exists(index):
        return FileResponse(index)
    return {"status": "CampusBuddy API running"}


@app.get("/api/status")
async def api_status():
    return {"status": "ready", "faces": face_count(), "face_enabled": FACE_ENABLED}


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    global _session_active, _is_registering

    await ws.accept()
    await ws.send_json({"type": "status", "message": "connected"})

    async def send(type_, **kwargs):
        await ws.send_json({"type": type_, **kwargs})

    loop = asyncio.get_event_loop()

    try:
        while True:
            data = await ws.receive_json()
            action = data.get("action")

            # ──────────────────────────────────────────
            # FIX: stop TTS immediately
            if action == "stop":
                stop_speech()
                await send("speech_stopped")
                continue

            # ──────────────────────────────────────────
            elif action == "identify":
                if not FACE_ENABLED:
                    await send("no_face")
                    continue

                cap = open_camera()
                if cap is None:
                    await send("no_face")
                    continue

                try:
                    ret, frame = cap.read()
                finally:
                    cap.release()

                if not ret or frame is None:
                    print("[CAMERA] Failed to read frame during identify.")
                    await send("no_face")
                    continue

                if face_count() == 0:
                    await send("no_face")
                    continue

                embedding = get_face_embedding(frame)
                if embedding is None:
                    await send("no_face")
                    continue

                meta, dist = find_closest_face(embedding)
                if meta and dist <= VERIFY_THRESHOLD:
                    _session_active = True  # FIX: pause wake word loop
                    await send(
                        "recognized",
                        name=meta["name"],
                        role=meta["role"],
                        branch=meta["branch"],
                        usn=meta.get("usn", ""),
                        verified=True,
                    )
                    await loop.run_in_executor(
                        None,
                        speak,
                        f"Welcome back, {meta['name']}! How can I help you?"
                    )
                    await send("speech_finished")  # FIX: tell frontend TTS is done
                else:
                    await send("no_face")

            # ──────────────────────────────────────────
            elif action == "check_wake":
                try:
                    _wake_queue.get_nowait()
                    _session_active = True  # FIX: session starts on wake
                    await send("wake_detected")
                except queue.Empty:
                    await send("wake_timeout")

            # ──────────────────────────────────────────
            elif action == "listen":
                async with _mic_lock:
                    await send("listening")
                    text = await loop.run_in_executor(None, listen_once)

                if not text:
                    await send("no_speech")
                    await send("auto_listen")
                    continue

                await send("transcribed", text=text)

                # FIX: detect goodbye/exit phrases
                text_lower = text.lower().strip()
                if any(phrase in text_lower for phrase in EXIT_PHRASES):
                    farewell = "Goodbye! Have a great day. Feel free to ask me anything next time!"
                    await send("answer", text=farewell)
                    await loop.run_in_executor(None, speak, farewell)
                    await send("speech_finished")
                    await send("goodbye")          # tells React to go back to idle
                    _session_active = False        # FIX: re-enable wake word loop
                    continue

                # FIX: detect registration intent
                if any(w in text_lower for w in ["register", "new user", "sign up", "enroll", "add face"]):
                    await send("start_register")
                    continue

                await send("thinking")
                chain = get_chain()
                answer = await loop.run_in_executor(None, ask, chain, text)
                answer_clean = clean(answer)
                tts_text = clean_for_tts(answer_clean)

                await send("answer", text=answer_clean)
                await loop.run_in_executor(None, speak, tts_text)
                await send("speech_finished")     # FIX: was missing — Stop button stuck
                await send("auto_listen")

            # ──────────────────────────────────────────
            elif action == "register_voice":
                if not FACE_ENABLED:
                    await send("register_failed", message="Face recognition is temporarily disabled.")
                    await loop.run_in_executor(None, speak, "Face recognition is temporarily disabled.")
                    continue

                # FIX: pause wake word loop during registration
                _is_registering = True

                # Check camera before starting
                test_cap = open_camera()
                if test_cap is None:
                    _is_registering = False
                    await send("register_failed", message="Camera not found. Please check the device.")
                    await loop.run_in_executor(None, speak, "Camera not found. Please connect a camera and try again.")
                    continue
                test_cap.release()

                info = {}

                async def ask_voice(question):
                    await send("register_ask", question=question)
                    await loop.run_in_executor(None, speak, question)
                    async with _mic_lock:
                        await send("listening")
                        ans = await loop.run_in_executor(None, listen_once)
                    await send("register_heard", value=ans if ans else "")
                    return ans or ""

                role_raw = await ask_voice("Are you a student or a teacher?")
                info["role"] = "Teacher" if "teach" in role_raw.lower() else "Student"
                info["name"] = await ask_voice("Please tell me your full name.")
                info["branch"] = await ask_voice("What is your branch or department?")

                if info["role"] == "Student":
                    info["usn"] = await ask_voice("What is your USN?")
                    info["designation"] = ""
                else:
                    info["designation"] = await ask_voice("What is your designation?")
                    info["usn"] = ""

                confirm_msg = (
                    f"I heard: Name {info['name']}, "
                    f"{info['role']}, {info['branch']}. "
                    f"Say yes to confirm or no to cancel."
                )
                confirmed = await ask_voice(confirm_msg)

                if "yes" not in confirmed.lower():
                    _is_registering = False
                    await send("register_cancelled", message="Registration cancelled.")
                    await loop.run_in_executor(None, speak, "Registration cancelled.")
                    continue

                ANGLES = ["straight", "left", "right", "up", "down"]
                ANGLE_INSTRUCTIONS = {
                    "straight": "Please look straight at the camera.",
                    "left": "Now slowly turn your head to the left.",
                    "right": "Now turn your head to the right.",
                    "up": "Now tilt your head up.",
                    "down": "Now tilt your head down.",
                }

                embeddings = []

                # FIX: open with CAP_DSHOW to prevent MSMF crash
                cap = open_camera()
                if cap is None:
                    _is_registering = False
                    await send("register_failed", message="Camera disconnected before capture.")
                    await loop.run_in_executor(None, speak, "Camera not available. Please check the device.")
                    continue

                face_cascade = cv2.CascadeClassifier(
                    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
                )

                camera_error = False

                for i, angle in enumerate(ANGLES):
                    instr = ANGLE_INSTRUCTIONS[angle]
                    progress = int(i / len(ANGLES) * 100)

                    await send("capture_angle", angle=angle, instruction=instr, progress=progress)
                    await loop.run_in_executor(None, speak, instr)

                    captured = False
                    attempts = 0

                    while not captured and attempts < 80:
                        ret, frame = cap.read()

                        if not ret or frame is None:
                            print(f"[CAMERA] Frame read failed at angle: {angle}")
                            camera_error = True
                            break

                        try:
                            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                            faces = face_cascade.detectMultiScale(gray, 1.1, 5)

                            if len(faces) > 0:
                                try:
                                    result = DeepFace.represent(
                                        img_path=frame,
                                        model_name="Facenet512",
                                        enforce_detection=True,
                                        detector_backend="opencv"
                                    )
                                    embeddings.append(result[0]["embedding"])
                                    captured = True
                                    progress_pct = int((i + 1) / len(ANGLES) * 100)
                                    await send("capture_progress", progress=progress_pct)
                                    await loop.run_in_executor(None, speak, "Got it.")
                                except Exception as e:
                                    print(f"[FACE] DeepFace error: {e}")
                        except Exception as e:
                            print(f"[CAMERA] Frame processing error: {e}")

                        attempts += 1
                        # FIX: small sleep to stop busy-loop hammering CPU
                        await asyncio.sleep(0.03)

                    if camera_error:
                        break

                cap.release()

                # FIX: always re-enable wake word loop after registration
                _is_registering = False

                if camera_error:
                    await send("register_failed", message="Camera stopped during capture.")
                    await loop.run_in_executor(None, speak, "Camera stopped working. Please check the connection.")
                    continue

                if len(embeddings) < 3:
                    await send("register_failed", message="Face capture failed. Try in better lighting.")
                    await loop.run_in_executor(None, speak, "Face capture failed. Please try again in better lighting.")
                    continue

                arr = np.array(embeddings)
                avg = np.mean(arr, axis=0)
                avg_emb = (avg / np.linalg.norm(avg)).tolist()
                person_id = str(uuid.uuid4())

                save_face(person_id, avg_emb, {
                    "name": info["name"],
                    "role": info["role"],
                    "branch": info["branch"],
                    "usn": info["usn"],
                    "designation": info["designation"],
                    "person_id": person_id
                })

                success_msg = f"Registration successful! Welcome to CampusBuddy, {info['name']}!"
                await send("register_success", name=info["name"])
                await loop.run_in_executor(None, speak, success_msg)
                await send("speech_finished")

    except WebSocketDisconnect:
        _session_active = False
        _is_registering = False
        print("[WS] Client disconnected")
    except Exception as e:
        print(f"[WS ERROR] {e}")
        _session_active = False
        _is_registering = False