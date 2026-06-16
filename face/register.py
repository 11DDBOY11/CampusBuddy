import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import uuid
import numpy as np
from deepface import DeepFace
from face.database import save_face
from gtts import gTTS
import pygame
import tempfile


ANGLES = ["straight", "left", "right", "up", "down"]
ANGLE_INSTRUCTIONS = {
    "straight": "Look straight at the camera",
    "left": "Now slowly turn your head to the LEFT",
    "right": "Now slowly turn your head to the RIGHT",
    "up": "Now tilt your head UP",
    "down": "Now tilt your head DOWN",
}


def speak_instruction(text):
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tmp = f.name
        tts.save(tmp)
        pygame.mixer.init()
        pygame.mixer.music.load(tmp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove(tmp)
    except Exception as e:
        print(f"[TTS] {e}")


def open_camera():
    """
    Attempt to open camera index 0.
    Returns the cap object if successful, or None if not available.
    """
    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 15)
        if not cap.isOpened():
            cap.release()
            print("[CAMERA] Camera not found or already in use.")
            return None
        return cap
    except Exception as e:
        print(f"[CAMERA] Exception opening camera: {e}")
        return None


def capture_faces_with_angles(label_var, progress_var, root):
    """
    Capture face embeddings across multiple head angles.
    Returns list of embeddings. Empty list means capture failed.
    """
    cap = open_camera()
    if cap is None:
        label_var.set("❌ Camera not found. Please connect a camera.")
        speak_instruction("Camera not found. Please connect a camera and try again.")
        return []

    embeddings = []
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    camera_error = False

    for i, angle in enumerate(ANGLES):
        instruction = ANGLE_INSTRUCTIONS[angle]
        label_var.set(f"📷 {instruction}")
        root.update()
        speak_instruction(instruction)

        captured = False
        attempts = 0

        while not captured and attempts < 100:
            ret, frame = cap.read()

            if not ret or frame is None:
                print(f"[CAMERA] Frame read failed at angle: {angle}")
                camera_error = True
                break

            try:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 5)

                cv2.imshow("CampusBuddy Registration - Press Q to skip angle", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

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
                        progress_var.set(int((i + 1) / len(ANGLES) * 100))
                        root.update()
                        speak_instruction("Got it!")
                    except Exception as e:
                        print(f"[FACE] DeepFace error at angle {angle}: {e}")

            except Exception as e:
                print(f"[CAMERA] Frame processing error: {e}")

            attempts += 1

        if camera_error:
            break

    cap.release()
    cv2.destroyAllWindows()

    if camera_error:
        label_var.set("❌ Camera stopped during capture. Check the connection.")
        speak_instruction("Camera stopped working. Please check the connection and try again.")
        return []

    return embeddings


def average_embedding(embeddings):
    arr = np.array(embeddings)
    avg = np.mean(arr, axis=0)
    return (avg / np.linalg.norm(avg)).tolist()


def open_registration_window():
    win = tk.Tk()
    win.title("CampusBuddy — Register Face")
    win.geometry("480x560")
    win.configure(bg="#1a1a2e")
    win.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background="#1a1a2e", foreground="white", font=("Segoe UI", 11))
    style.configure("TEntry", font=("Segoe UI", 11))
    style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=8)
    style.configure("TCombobox", font=("Segoe UI", 11))

    tk.Label(win, text="🎓 CampusBuddy Registration", bg="#1a1a2e",
             fg="#00d4ff", font=("Segoe UI", 15, "bold")).pack(pady=15)

    role_var = tk.StringVar(value="Student")
    name_var = tk.StringVar()
    usn_var = tk.StringVar()
    branch_var = tk.StringVar()
    desig_var = tk.StringVar()

    form_frame = tk.Frame(win, bg="#1a1a2e")
    form_frame.pack(padx=30, fill="x")

    def make_label_entry(parent, label, textvariable):
        row = tk.Frame(parent, bg="#1a1a2e")
        row.pack(fill="x", pady=5)
        tk.Label(row, text=label, bg="#1a1a2e", fg="white",
                 font=("Segoe UI", 10), width=16, anchor="w").pack(side="left")
        entry = ttk.Entry(row, textvariable=textvariable)
        entry.pack(side="left", fill="x", expand=True)
        return row

    make_label_entry(form_frame, "Full Name *", name_var)

    role_row = tk.Frame(form_frame, bg="#1a1a2e")
    role_row.pack(fill="x", pady=5)
    tk.Label(role_row, text="Role *", bg="#1a1a2e", fg="white",
             font=("Segoe UI", 10), width=16, anchor="w").pack(side="left")
    role_combo = ttk.Combobox(role_row, textvariable=role_var,
                               values=["Student", "Teacher", "Staff"], state="readonly")
    role_combo.pack(side="left", fill="x", expand=True)

    usn_row = tk.Frame(form_frame, bg="#1a1a2e")
    tk.Label(usn_row, text="USN *", bg="#1a1a2e", fg="white",
             font=("Segoe UI", 10), width=16, anchor="w").pack(side="left")
    ttk.Entry(usn_row, textvariable=usn_var).pack(side="left", fill="x", expand=True)

    desig_row = tk.Frame(form_frame, bg="#1a1a2e")
    tk.Label(desig_row, text="Designation *", bg="#1a1a2e", fg="white",
             font=("Segoe UI", 10), width=16, anchor="w").pack(side="left")
    ttk.Entry(desig_row, textvariable=desig_var).pack(side="left", fill="x", expand=True)

    make_label_entry(form_frame, "Branch/Dept *", branch_var)

    def toggle_fields(*args):
        usn_row.pack_forget()
        desig_row.pack_forget()
        if role_var.get() == "Student":
            usn_row.pack(fill="x", pady=5)
        else:
            desig_row.pack(fill="x", pady=5)

    role_var.trace("w", toggle_fields)
    toggle_fields()

    status_var = tk.StringVar(value="Fill the form and click Register")
    progress_var = tk.IntVar(value=0)

    tk.Label(win, textvariable=status_var, bg="#1a1a2e", fg="#ffd700",
             font=("Segoe UI", 10), wraplength=420).pack(pady=10)
    ttk.Progressbar(win, variable=progress_var, maximum=100,
                    length=380).pack(pady=5)

    def start_registration():
        name = name_var.get().strip()
        role = role_var.get()
        branch = branch_var.get().strip()
        usn = usn_var.get().strip()
        desig = desig_var.get().strip()

        if not name or not branch:
            messagebox.showerror("Error", "Name and Branch are required!")
            return
        if role == "Student" and not usn:
            messagebox.showerror("Error", "USN is required for students!")
            return
        if role in ["Teacher", "Staff"] and not desig:
            messagebox.showerror("Error", "Designation is required!")
            return

        def run():
            status_var.set("📷 Starting camera... get ready!")
            progress_var.set(0)
            win.update()

            embeddings = capture_faces_with_angles(status_var, progress_var, win)

            if len(embeddings) < 3:
                if "Camera" not in status_var.get():
                    status_var.set("❌ Could not capture enough angles. Try again.")
                return

            avg_emb = average_embedding(embeddings)
            person_id = str(uuid.uuid4())
            metadata = {
                "name": name,
                "role": role,
                "branch": branch,
                "usn": usn if role == "Student" else "",
                "designation": desig if role != "Student" else "",
                "person_id": person_id
            }
            save_face(person_id, avg_emb, metadata)
            status_var.set(f"✅ {name} registered successfully!")
            speak_instruction(f"Registration successful! Welcome to CampusBuddy, {name}!")
            progress_var.set(100)

        threading.Thread(target=run, daemon=True).start()

    ttk.Button(win, text="📸 Register Face", command=start_registration).pack(pady=15)
    win.mainloop()


if __name__ == "__main__":
    open_registration_window()