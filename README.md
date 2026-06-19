# 🧠 OmniMind — Personal AI Research Assistant

> A production-ready AI assistant that combines **RAG**, **Long-Term Memory**,
> and a **Multi-Agent Architecture** to answer questions from your documents intelligently.

---

## ✨ Features

- 📄 **Document Ingestion** — Upload PDF, TXT, and DOCX files
- 🔍 **RAG Pipeline** — Semantic search over your knowledge base
- 🧠 **Memory System** — Short-term + Long-term memory
- 🤖 **Multi-Agent System** — Researcher, Summarizer, FactChecker, Orchestrator
- ⚡ **FastAPI Backend** — High-performance REST API
- 💬 **Modern Chat UI** — Clean ChatGPT-style interface
- 🐳 **Docker Support** — Run everything with a single command
- 🔓 **Fully Open Source** — Runs locally using Ollama

---

# 🏗️ Architecture

```text
omnimind/
│
├── core/
│   ├── config.py
│   └── logger.py
│
├── models/
│   └── ollama_model.py
│
├── memory/
│   ├── short_term.py
│   └── long_term.py
│
├── rag/
│   ├── loader.py
│   ├── chunker.py
│   ├── embedder.py
│   └── retriever.py
│
├── agents/
│   ├── researcher.py
│   ├── summarizer.py
│   ├── fact_checker.py
│   └── orchestrator.py
│
├── api/
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# 🚀 Quick Start

## Option 1 — Local Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Mo7239/OmniMind.git

cd omnimind
```

### 2️⃣ Create a Virtual Environment

#### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

#### Linux / macOS

```bash
cp .env.example .env
```

#### Windows (PowerShell)

```powershell
Copy-Item .env.example .env
```

### 5️⃣ Pull the Ollama Model

```bash
ollama pull mistral
```

### 6️⃣ Run the Application

```bash
uvicorn api.main:app --reload --port 8000
```

Open:

```text
http://localhost:8000
```

---

## Option 2 — Docker

```bash
docker compose up --build
```

Then open:

```text
http://localhost:8000
```

---

# 🤖 Agent System

| Agent | Responsibility |
|---------|---------|
| 🔍 Researcher | Retrieves relevant information from documents |
| 📝 Summarizer | Generates concise summaries |
| ✅ FactChecker | Verifies claims against sources |
| 🎯 Orchestrator | Coordinates all agents and workflow |

---

# 🛠️ Tech Stack

| Layer | Technology |
|---------|---------|
| LLM | Ollama + Mistral |
| Embeddings | all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| Backend | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Containerization | Docker |
| Language | Python 3.11+ |

---

# 📡 API Endpoints

| Method | Endpoint | Description |
|----------|----------|----------|
| GET | `/health` | Health Check |
| POST | `/chat` | Send a Chat Message |
| GET | `/history` | Retrieve Chat History |
| DELETE | `/history` | Clear Chat History |
| POST | `/upload` | Upload Documents |

---


