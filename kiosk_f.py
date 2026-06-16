import os
import sys
import subprocess
import threading
import time
import webbrowser

def start_backend():
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "api.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])

def open_browser():
    time.sleep(3)
    webbrowser.open("http://localhost:3000")

if __name__ == "__main__":
    print("=" * 55)
    print("🎓 CampusBuddy Kiosk — Starting...")
    print("=" * 55)
    print("\n📡 Starting FastAPI backend on port 8000...")
    print("🌐 Opening UI on http://localhost:3000")
    print("\nPress Ctrl+C to stop\n")

    threading.Thread(target=open_browser, daemon=True).start()
    start_backend()
