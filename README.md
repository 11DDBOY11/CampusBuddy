# 🎓 CampusBuddy - Phase 1 (RAG Backend)
AI-powered campus assistant for AIET using LangChain + ChromaDB + Ollama (Llama 3.2).
Completely free. Runs 100% locally. No API keys needed.

---

## 🛠️ Setup Instructions

### 1. Install Ollama
Download from https://ollama.com and run:
```
ollama pull llama3.2
```

### 2. Install Python dependencies
```
pip install -r requirements.txt
```

### 3. Scrape AIET website data
```
python data/scraper.py
```

### 4. Ingest data into ChromaDB
```
python rag/ingest.py
```

### 5. Start CampusBuddy
```
python main.py
```

---

## 💬 Sample Questions to Try
- What is AIET?
- What departments are available?
- Where is the college located?
- What are the facilities at AIET?
- How can I contact the admissions office?

---

## 📁 Project Structure
```
campusbuddy/
├── data/
│   ├── scraper.py       # Scrapes AIET website
│   └── scraped/         # Scraped text files (auto-generated)
├── rag/
│   ├── ingest.py        # Embeds data into ChromaDB
│   └── query.py         # RAG query engine
├── main.py              # Terminal chat interface
└── requirements.txt
```

---
Built by: Darshan Dashyal | AIET | 4AL23CS035
