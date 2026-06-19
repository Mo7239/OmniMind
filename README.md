# 🧠 OmniMind — Personal AI Research Assistant

OmniMind is a production-ready AI assistant that combines RAG, long-term memory,
and a multi-agent system to answer questions from your documents intelligently.

---

## ✨ Features

- 📄 **Document Ingestion** — Upload PDF, TXT, DOCX files
- 🔍 **RAG Pipeline** — Semantic search over your documents
- 🧠 **Memory System** — Short-term (conversation) + Long-term (vector DB)
- 🤖 **Multi-Agent System** — Researcher, Summarizer, FactChecker
- ⚡ **FastAPI Backend** — REST API with auto docs
- 💬 **ChatGPT-like UI** — Clean chat interface
- 🐳 **Dockerized** — One command to run everything
- 🔓 **100% Open Source** — Runs locally with Ollama

---

## 🏗️ Project Structure

\`\`\`
omnimind/
├── core/               # Config & Logger
├── models/             # LLM abstraction (Ollama)
├── memory/             # Short-term & Long-term memory
├── rag/                # Document loader, chunker, embedder, retriever
├── agents/             # Researcher, Summarizer, FactChecker, Orchestrator
├── api/                # FastAPI routes
├── frontend/           # HTML, CSS, JS Chat UI
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
\`\`\`

---

## 🚀 Quick Start

### Option 1: Local

**1. Clone the repo**
\`\`\`bash
git clone https://github.com/yourusername/omnimind.git
cd omnimind
\`\`\`

**2. Create virtual environment**
\`\`\`bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
\`\`\`

**3. Install dependencies**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

**4. Setup environment**
\`\`\`bash
cp .env.example .env
\`\`\`

**5. Pull Ollama model**
\`\`\`bash
ollama pull mistral
\`\`\`

**6. Run the app**
\`\`\`bash
uvicorn api.main:app --reload --port 8000
\`\`\`

---

### Option 2: Docker

\`\`\`bash
docker-compose up --build
\`\`\`

Open your browser at `http://localhost:8000`

---

## 🤖 Agents

| Agent | Trigger Keywords | Role |
|-------|-----------------|------|
| 🔍 Researcher | any question | Searches documents and answers |
| 📝 Summarizer | summarize, تلخيص | Summarizes conversation |
| ✅ FactChecker | verify, تحقق, fact | Verifies claims against documents |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Ollama + Mistral 7B |
| Embeddings | all-MiniLM-L6-v2 |
| Vector DB | ChromaDB |
| Backend | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Container | Docker + docker-compose |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/health` | Health check |
| POST | `/chat` | Send a message |
| GET | `/history` | Get chat history |
| DELETE | `/history` | Clear chat history |
| POST | `/upload` | Upload a document |

---

