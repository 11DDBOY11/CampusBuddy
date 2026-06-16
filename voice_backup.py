import os
os.environ["PATH"] += os.pathsep + r"C:\Users\dkk82\AppData\Local\Microsoft\WinGet\Links"

import sys
import tempfile
from faster_whisper import WhisperModel
import speech_recognition as sr
from gtts import gTTS
import pygame


# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rag.query import load_rag_chain, ask

# ── Audio config ─────────────────────────────────────────────
WHISPER_MODEL = "base"   # tiny / base / small — base is best balance
LANGUAGE      = "en"
TTS_LANG      = "en"
TTS_SLOW      = False

import re

def clean_text(text: str) -> str:
    text = re.sub(r'\*+', '', text)        # remove * and **
    text = re.sub(r'#+\s*', '', text)      # remove ## headers
    text = re.sub(r'\n+', '. ', text)      # newlines to pauses
    text = re.sub(r'\s+', ' ', text)       # clean extra spaces
    return text.strip()

# ── TTS: speak text aloud ────────────────────────────────────
def speak(text: str):
    print(f"CampusBuddy: {text}")
    try:
        tts = gTTS(text=text, lang=TTS_LANG, slow=TTS_SLOW)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tmp_path = f.name
        tts.save(tmp_path)

        pygame.mixer.init()
        pygame.mixer.music.load(tmp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove(tmp_path)
    except Exception as e:
        print(f"[TTS Error] {e}")

# ── STT: capture mic and transcribe with Whisper ─────────────
def listen(whisper_model) -> str:
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.pause_threshold  = 1.0

    with sr.Microphone() as source:
        print("\n🎤 Listening... (speak now)")
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
    text = " ".join([seg.text for seg in segments]).strip()
    os.remove(tmp_wav)
    text = clean_text(text)
    print(f"You said: {text}")
    return text

# ── Main voice loop ──────────────────────────────────────────
def main():
    print("=" * 52)
    print("🎓 CampusBuddy - AIET Voice Assistant")
    print("   Say 'exit' or 'bye' to quit")
    print("=" * 52)

    print("\n⏳ Loading RAG engine...")
    chain = load_rag_chain()
    print("⏳ Loading Whisper STT model...")
    whisper_model = WhisperModel("tiny", device="cpu", compute_type="int8")
    print("✅ CampusBuddy Voice is ready!\n")

    speak("Hello! I am CampusBuddy, your AI assistant for Alva's Institute of Engineering and Technology. How can I help you today?")

    while True:
        text = listen(whisper_model)

        if not text:
            speak("Sorry, I didn't catch that. Please try again.")
            continue

        if any(word in text.lower() for word in ["exit", "bye", "quit", "goodbye"]):
            speak("Goodbye! Have a great day at AIET!")
            break

        print("⏳ Thinking...")
        answer = ask(chain, text)
        speak(clean_text(answer))

if __name__ == "__main__":
    main()
