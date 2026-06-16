<div align="center">

<img src="ui/src/assets/logo.png" alt="CampusBuddy Logo" width="120"/>

# 🤖 CampusBuddy
### AI-Powered Campus Kiosk Assistant for AIET, Moodubidri

[
[
[
[
[
[

> A fully offline, voice-activated AI assistant kiosk for Alva's Institute of Engineering and Technology.  
> Greets visitors by name using face recognition. Answers questions using RAG over real college data.  
> No internet. No API keys. Just plug in and talk.

</div>

***

## ✨ Features

| Feature | Description |
|---|---|
| 🎙️ Wake Word Detection | Say **"Hey Campus Buddy"** to activate |
| 🧠 RAG-Powered QA | Answers questions from real AIET website data using LangChain + ChromaDB |
| 🔊 Voice Output | Responds in natural spoken English using gTTS + pygame |
| 👁️ Face Recognition | Identifies registered students and faculty using DeepFace + FaceNet512 |
| 📋 Voice Registration | New users can register face + details entirely by voice |
| 💬 WebSocket Real-Time | Live status updates between React UI and FastAPI backend |
| 🖥️ Kiosk UI | Fullscreen React UI with IdleScreen, ActiveScreen, and status overlays |
| 📴 100% Offline | Runs entirely on local hardware — no cloud, no API keys needed |

***

## 🏗️ Tech Stack

### Backend
- **FastAPI** — WebSocket server and REST API
- **LangChain + ChromaDB** — RAG pipeline for AIET knowledge base
- **Ollama (Llama 3.2:1b)** — Local LLM for answer generation
- **HuggingFace (all-MiniLM-L6-v2)** — Sentence embeddings
- **DeepFace (FaceNet512)** — Face recognition and embedding
- **faster-whisper** — Offline speech-to-text (STT)
- **gTTS + pygame** — Text-to-speech (TTS) playback
- **OpenCV** — Camera capture and face detection

### Frontend
- **React 18** — Kiosk UI with multiple screen states
- **WebSocket** — Real-time communication with backend
- **CSS Animations** — Smooth transitions between IdleScreen and ActiveScreen

***

## 📁 Project Structure

```
campusbuddy/
│
├── server/
│   └── main.py              ← FastAPI WebSocket server (entry point)
│
├── rag/
│   ├── ingest.py            ← Embeds AIET data into ChromaDB
│   └── query.py             ← RAG chain (LangChain + Ollama)
│
├── face/
│   ├── recognize.py         ← DeepFace embedding extraction
│   └── database.py          ← SQLite face store (save/find/count)
│
├── api/
│   ├── stt.py               ← Speech-to-text (faster-whisper + wake word)
│   └── tts.py               ← Text-to-speech (gTTS + pygame)
│
├── data/
│   ├── scraped/             ← Raw AIET website text files
│   └── chroma_db/           ← ChromaDB vector store (auto-generated)
│
├── ui/
│   ├── src/
│   │   ├── components/
│   │   │   ├── IdleScreen.js    ← Kiosk idle display
│   │   │   └── ActiveScreen.js  ← Active conversation display
│   │   └── App.js
│   └── package.json
│
├── scraper.py               ← Scrapes AIET website data
├── kiosk_f.py               ← One-click launcher (backend + browser)
├── check.py                 ← Dependency checker
├── requirements.txt
└── README.md
```

***

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.com/) installed and running
- A webcam connected to the system
- A microphone connected to the system

***

### Step 1 — Clone the repository

```bash
git clone https://github.com/11DDBOY11/CampusBuddy.git
cd CampusBuddy
```

### Step 2 — Create and activate virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate.bat

# Linux / Mac
source .venv/bin/activate
```

### Step 3 — Install Python dependencies

```bash
pip install -r requirements.txt
pip install tensorflow==2.15.0 keras==2.15.0
pip install deepface==0.0.79
```

### Step 4 — Pull the LLM model via Ollama

```bash
ollama pull llama3.2:1b
```

### Step 5 — Scrape AIET website data

```bash
python scraper.py
```

### Step 6 — Ingest data into ChromaDB

```bash
python rag/ingest.py
```

### Step 7 — Install React frontend

```bash
cd ui
npm install
cd ..
```

***

## 🚀 Running the Project

### Option A — One-click launcher

```bash
python kiosk_f.py
```

### Option B — Manual (two terminals)

**Terminal 1 — Backend:**
```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 — Frontend:**
```bash
cd ui
npm start
```

Then open **http://localhost:3000** in your browser.

***

## 🎤 How to Use

1. The kiosk starts in **IdleScreen** — showing campus information
2. Say **"Hey Campus Buddy"** to wake it up
3. Ask any question about AIET — departments, placements, facilities, events, hostel, etc.
4. CampusBuddy responds in spoken English
5. For **face registration**, say *"register"* or *"new user"* — the system will guide you by voice through capturing your face and saving your details
6. Once registered, the kiosk will **greet you by name** next time it sees your face

***

## 🧪 Verify Installation

Run the dependency checker:

```bash
python check.py
```

Quick DeepFace test:
```bash
python -c "from deepface import DeepFace; print('DeepFace OK')"
```

***

## 📸 Sample Questions to Ask

- *"What departments are available at AIET?"*
- *"Tell me about the placement record"*
- *"What are the facilities on campus?"*
- *"Who is the principal of AIET?"*
- *"How do I apply for admission?"*
- *"What is the hostel facility like?"*
- *"Tell me about the Pragati placement drive"*

***

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `uvicorn: app not found` | Use `python -m uvicorn api.main:app --port 8000` |
| Camera error `-1072873851` | Use `cv2.VideoCapture(0, cv2.CAP_DSHOW)` on Windows |
| DeepFace import error | Run `pip install tensorflow==2.15.0 deepface==0.0.79` |
| Wake word not detecting | Check mic input device, speak clearly — *"Hey Campus Buddy"* |
| Ollama not responding | Run `ollama serve` in a separate terminal first |
| ChromaDB empty | Re-run `python scraper.py` then `python rag/ingest.py` |

***

## 👨‍💻 Author

**Darshan Dashyal**  
B.E. Computer Science Engineering  
Alva's Institute of Engineering and Technology, Moodubidri  
USN: `4AL23CS035`

***

## 📄 License

This project is licensed under the [MIT License](LICENSE).

***

<div align="center">

Built with ❤️ at AIET, Moodubidri · Powered by Llama 3.2 · Runs 100% Locally

⭐ Star this repo if you found it useful!

</div>
