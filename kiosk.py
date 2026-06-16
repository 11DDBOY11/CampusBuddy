import os
import sys

os.environ["PATH"] += os.pathsep + r"C:\Users\dkk82\AppData\Local\Microsoft\WinGet\Links"

import threading
import re
import tempfile
import time
import cv2
import pygame
from gtts import gTTS
from faster_whisper import WhisperModel
import speech_recognition as sr

from rag.query import load_rag_chain, ask
from face.recognize import run_recognition_loop
from face.register import open_registration_window

LANGUAGE = "en"

def clean_text(text: str) -> str:
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"#+\s*", "", text)
    text = re.sub(r"\n+", ". ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def speak(text: str):
    print(f"CampusBuddy: {text}")
    try:
        tts = gTTS(text=text, lang=LANGUAGE, slow=False)
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
        print(f"[TTS Error] {e}")

def listen(whisper_model) -> str:
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 1.0
    with sr.Microphone() as source:
        print("\n🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            return ""
    print("⏳ Transcribing...")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        tmp_wav = f.name
    with open(tmp_wav, "wb") as f:
        f.write(audio.get_wav_data())
    segments, _ = whisper_model.transcribe(tmp_wav, language=LANGUAGE)
    os.remove(tmp_wav)
    text = " ".join([seg.text for seg in segments]).strip()
    print(f"You said: {text}")
    return text

def start_voice_session(chain, whisper_model, person_info):
    name = person_info.get("name", "there")
    if person_info.get("verified"):
        greeting = f"Welcome back, {name}! How can I help you today?"
    else:
        greeting = "Hello! Welcome to AIET. I am CampusBuddy. How can I help you?"
    speak(greeting)
    while True:
        question = listen(whisper_model)
        if not question:
            speak("Sorry, I didn't catch that. Please try again.")
            continue
        if any(w in question.lower() for w in ["exit", "bye", "quit", "goodbye", "thank you"]):
            speak(f"Goodbye {name}! Have a great day!")
            break
        print("⏳ Thinking...")
        answer = ask(chain, question)
        speak(clean_text(answer))

def main():
    print("=" * 55)
    print("🎓 CampusBuddy Kiosk — AIET")
    print("   1. Start Kiosk (Face Recognition + Voice)")
    print("   2. Register New Face")
    print("   3. Exit")
    print("=" * 55)

    choice = input("Choose option (1/2/3): ").strip()

    if choice == "2":
        open_registration_window()
        return
    if choice == "3":
        return

    print("\n⏳ Loading RAG engine...")
    chain = load_rag_chain()
    print("⏳ Loading Whisper STT...")
    whisper_model = WhisperModel("tiny", device="cpu", compute_type="int8")
    print("✅ CampusBuddy Kiosk is ready!\n")
    speak("CampusBuddy kiosk is now active. Please look at the camera.")

    def on_face_recognized(person_info):
        start_voice_session(chain, whisper_model, person_info)

    run_recognition_loop(on_face_recognized)

if __name__ == "__main__":
    main()