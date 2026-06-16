"""
Run this file directly to test your microphone setup:
  python diagnosis/mic_test.py
"""
import speech_recognition as sr

r = sr.Recognizer()

print("\n=== AVAILABLE MICROPHONES ===")
mics = sr.Microphone.list_microphone_names()
for i, name in enumerate(mics):
    print(f"  [{i}] {name}")

print("\n=== TESTING DEFAULT MICROPHONE ===")
print("Speak something within 5 seconds...")

try:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print(f"Energy threshold: {r.energy_threshold:.0f}")
        print("GO! (speak now)")
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
    result = r.recognize_google(audio, language="en-IN")
    print(f"\n✅ SUCCESS! Heard: '{result}'")
except sr.WaitTimeoutError:
    print("\n❌ TIMEOUT: No speech detected.")
    print("   → Possible fix: Speak louder or closer to the mic")
    print("   → Or set a specific device index (see list above)")
except sr.UnknownValueError:
    print("\n⚠️  COULD NOT UNDERSTAND: Mic is working but speech unclear.")
except sr.RequestError as e:
    print(f"\n❌ GOOGLE API ERROR: {e}")
    print("   → Are you connected to the internet?")
except OSError as e:
    print(f"\n❌ MIC NOT FOUND: {e}")
    print("   → Check if mic is plugged in / enabled in Windows settings")