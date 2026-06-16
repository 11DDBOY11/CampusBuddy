import os
import tempfile
import speech_recognition as sr
from faster_whisper import WhisperModel

from utils.network import is_online

_whisper_model = None
_recognizer = sr.Recognizer()
_recognizer.dynamic_energy_threshold = False
_recognizer.energy_threshold = 300
_recognizer.pause_threshold = 1.0

def get_whisper():
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
    return _whisper_model

def listen_wake_word(timeout=3) -> bool:
    WAKE_WORDS = ["campus buddy", "campusbuddy", "hello buddy", "hey buddy", "start", "hello", "hi buddy"]
    try:
        with sr.Microphone() as source:
            _recognizer.adjust_for_ambient_noise(source, duration=0.3)
            _recognizer.energy_threshold = max(200, min(_recognizer.energy_threshold, 400))
            audio = _recognizer.listen(source, timeout=timeout, phrase_time_limit=4)
    except sr.WaitTimeoutError:
        return False
    except OSError as e:
        print(f"[WAKE] Mic error: {e}")
        return False

    # FIX: skip Google entirely if offline — avoids long timeout, use Whisper instead
    if is_online():
        try:
            text = _recognizer.recognize_google(audio, language="en-IN").lower()
            print(f"[WAKE] (online) Heard: '{text}'")
            return any(w in text for w in WAKE_WORDS)
        except sr.UnknownValueError:
            return False
        except sr.RequestError as e:
            print(f"[WAKE] Google API error: {e} — falling back to Whisper.")
        except Exception as e:
            print(f"[WAKE] Error: {e} — falling back to Whisper.")

    # Offline fallback — local Whisper
    tmp_wav = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            tmp_wav = f.name
            f.write(audio.get_wav_data())
        model = get_whisper()
        segments, _ = model.transcribe(tmp_wav, language="en", vad_filter=True)
        text = " ".join(s.text for s in segments).strip().lower()
        print(f"[WAKE] (offline) Heard: '{text}'")
        return any(w in text for w in WAKE_WORDS)
    except Exception as e:
        print(f"[WAKE] Whisper error: {e}")
        return False
    finally:
        if tmp_wav and os.path.exists(tmp_wav):
            try:
                os.remove(tmp_wav)
            except Exception:
                pass

def listen_once(timeout=8, phrase_time_limit=15) -> str:
    tmp_wav = None
    try:
        with sr.Microphone() as source:
            _recognizer.adjust_for_ambient_noise(source, duration=0.5)
            _recognizer.energy_threshold = max(200, min(_recognizer.energy_threshold, 400))
            print(f"[STT] Listening... threshold={_recognizer.energy_threshold:.0f}")
            try:
                audio = _recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            except sr.WaitTimeoutError:
                print("[STT] Timeout")
                return ""
    except OSError as e:
        print(f"[STT] Mic error: {e}")
        return ""

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            tmp_wav = f.name
            f.write(audio.get_wav_data())
        model = get_whisper()
        segments, _ = model.transcribe(tmp_wav, language="en", beam_size=5, vad_filter=True)
        text = " ".join(s.text for s in segments).strip()
        print(f"[STT] Recognized: '{text}'")
        return text
    except Exception as e:
        print(f"[STT] Whisper error: {e}")
        return ""
    finally:
        if tmp_wav and os.path.exists(tmp_wav):
            try:
                os.remove(tmp_wav)
            except Exception:
                pass