# 🎤 CampusBuddy - Phase 2 (Voice Layer)
Adds voice interaction on top of Phase 1 RAG backend.
Uses Whisper (STT) + gTTS (TTS) + PyAudio (mic input).

# 📋 Prerequisites
Phase 1 must be fully working before this step.

# 🛠️ Setup
1. Install Phase 2 dependencies
text
pip install -r requirements_phase2.txt
2. Install FFmpeg (required by Whisper)
Download from https://ffmpeg.org/download.html
Add to system PATH or place ffmpeg.exe in project folder.

Windows quick install via winget:

text
winget install ffmpeg
3. Copy voice.py into your campusbuddy/ folder
Place voice.py alongside main.py in the root project folder.

4. Run voice mode
Make sure Ollama is running, then:

text
python voice.py
🎤 How It Works
CampusBuddy greets you with a welcome message

Speaks "Listening..." and waits for your question

Whisper transcribes your speech to text (local, offline)

RAG chain finds answer from AIET data

gTTS converts answer to audio and plays it back

⚙️ Whisper Model Options (in voice.py line 13)
Model	Size	Speed	Accuracy
tiny	75MB	Fast	Basic
base	145MB	Good	Good ✅
small	465MB	Slow	Better
Default is base — best balance for a kiosk.

📁 Files Added
voice.py — Voice assistant interface

requirements_phase2.txt — New dependencies

README_phase2.md — This guide

All Phase 1 files remain unchanged.
main.py (text mode) still works as before.

Built by: Darshan Dashyal | AIET | 4AL23CS035