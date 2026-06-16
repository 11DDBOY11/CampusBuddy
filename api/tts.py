import os
import tempfile
import time
from gtts import gTTS
import pygame

from utils.network import is_online

_stop_flag = False

def stop_speech():
    global _stop_flag
    _stop_flag = True
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
    except Exception:
        pass

def _speak_offline(text: str):
    """Offline TTS using pyttsx3 (Windows SAPI voices)."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", 165)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[TTS Error - offline] {e}")


def speak(text: str):
    global _stop_flag
    _stop_flag = False

    if not text or not text.strip():
        return

    # FIX: fast pre-check — skip gTTS entirely if offline (avoids long DNS timeout)
    if not is_online():
        print("[TTS] Offline — using pyttsx3.")
        _speak_offline(text)
        return

    tmp_path = None
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tmp_path = f.name
        tts.save(tmp_path)

        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.load(tmp_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if _stop_flag:
                pygame.mixer.music.stop()
                break
            time.sleep(0.05)

        if pygame.mixer.get_init():
            try:
                pygame.mixer.music.unload()
            except Exception:
                pass

    except Exception as e:
        print(f"[TTS] gTTS failed ({e}), falling back to offline.")
        _speak_offline(text)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass