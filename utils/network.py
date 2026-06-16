"""
Network connectivity helper for CampusBuddy.
Used to decide whether to use online services (Google STT, gTTS)
or fall back to fully offline alternatives (Whisper, pyttsx3).
"""

import socket
import time

_last_check = 0
_last_result = False
_CACHE_SECONDS = 5  # avoid checking on every single call


def is_online(force=False) -> bool:
    """
    Quick check for internet connectivity.
    Caches result for a few seconds so we don't add latency
    to every TTS/STT call.
    """
    global _last_check, _last_result

    now = time.time()
    if not force and (now - _last_check) < _CACHE_SECONDS:
        return _last_result

    try:
        # DNS resolution + connection to a fast, reliable host
        socket.setdefaulttimeout(1.5)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        _last_result = True
    except OSError:
        _last_result = False

    _last_check = now
    return _last_result