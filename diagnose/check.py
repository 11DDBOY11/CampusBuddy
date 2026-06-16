import importlib
import subprocess
import sys
import os

PACKAGES = [
    ("fastapi",             "fastapi"),
    ("uvicorn",             "uvicorn"),
    ("numpy",               "numpy"),
    ("opencv-python",       "cv2"),
    ("SpeechRecognition",   "speech_recognition"),
    ("faster-whisper",      "faster_whisper"),
    ("gTTS",                "gtts"),
    ("pygame",              "pygame"),
    ("pyaudio",             "pyaudio"),
    ("ollama",              "ollama"),
    ("transformers",        "transformers"),
    ("huggingface_hub",     "huggingface_hub"),
    ("langchain",           "langchain"),
    ("langchain-community", "langchain_community"),
    ("langchain-chroma",    "langchain_chroma"),
    ("chromadb",            "chromadb"),
    ("tensorflow-cpu",      "tensorflow"),
    ("keras",               "keras"),
    ("sentence-transformers", "sentence_transformers"),
    ("deepface",            "deepface"),
]

SERVICES = [
    ("Ollama service",  ["ollama", "list"]),
]

def check_packages():
    print("\n========== PYTHON PACKAGES ==========")
    all_ok = True
    for pkg_name, import_name in PACKAGES:
        try:
            mod = importlib.import_module(import_name)
            version = getattr(mod, "__version__", "installed")
            print(f"  [OK]      {pkg_name:<25} -> {version}")
        except Exception as e:
            print(f"  [MISSING] {pkg_name:<25} -> {e}")
            all_ok = False
    return all_ok

def check_services():
    print("\n========== EXTERNAL SERVICES ==========")
    for name, cmd in SERVICES:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"  [OK]      {name}")
            else:
                print(f"  [ERROR]   {name} -> {result.stderr.strip()}")
        except FileNotFoundError:
            print(f"  [MISSING] {name} -> command not found")
        except subprocess.TimeoutExpired:
            print(f"  [TIMEOUT] {name} -> did not respond in 5s")
        except Exception as e:
            print(f"  [ERROR]   {name} -> {e}")

def check_env():
    print("\n========== ENVIRONMENT ==========")
    print(f"  Python     : {sys.version}")
    print(f"  Executable : {sys.executable}")
    venv = os.environ.get("VIRTUAL_ENV", "NOT in a venv")
    print(f"  Venv       : {venv}")

if __name__ == "__main__":
    check_env()
    packages_ok = check_packages()
    check_services()
    print("\n========== SUMMARY ==========")
    if packages_ok:
        print("  All packages are present.")
    else:
        print("  Some packages are MISSING. Install them and re-run this script.")
    print()