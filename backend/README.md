# 🏥 Medical Chatbot — Backend

FastAPI-powered REST API for the AI medical chatbot. Uses **LangChain**, **Ollama** (local LLM), **ChromaDB** (vector store), and **PostgreSQL** to provide a secure, RAG-based conversational medical assistant.

---

## 📋 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Directory Structure](#-directory-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Database Setup](#-database-setup)
- [Adding Medical Documents](#-adding-medical-documents)
- [Running the Server](#-running-the-server)
- [API Reference](#-api-reference)
- [RAG Pipeline](#-rag-pipeline)
- [Authentication Flow](#-authentication-flow)
- [Admin Endpoints](#-admin-endpoints)
- [Testing](#-testing)

---

## 🏗️ Architecture Overview

```
Request → FastAPI Router → Safety Validator
                              ↓
                        RAG Pipeline
                    ┌─────────────────────┐
                    │  ChromaDB (vectors) │
                    │  + Ollama LLM       │
                    │  + LangChain Chain  │
                    └─────────────────────┘
                              ↓
                    Response Analyzer → PostgreSQL (save)
                              ↓
                         JSON Response
```

**Key components:**
- **LLM:** `llama3.2:1b` via Ollama (runs locally, no API key needed)
- **Embeddings:** `nomic-embed-text` via Ollama
- **Vector Store:** ChromaDB (persisted to `db/` directory)
- **Memory:** Per-session `ConversationBufferWindowMemory` (last 4 Q&A pairs)
- **Database:** PostgreSQL via SQLModel ORM

---

## 📁 Directory Structure

```
backend/
├── main.py                     # Server entry point (Uvicorn)
├── setup_database.sh           # PostgreSQL setup script
├── setup_api.sh                # API setup helper
├── verify_api.py               # API smoke test script
├── data/                       # Place your PDF documents here
├── db/                         # ChromaDB vector store (auto-created)
├── logs/                       # Rotating daily log files (auto-created)
└── src/
    ├── api/
    │   ├── __init__.py         # FastAPI app factory (create_app)
    │   ├── middleware.py       # CORS, error handling middleware
    │   ├── dependencies.py     # FastAPI dependency injection
    │   ├── models/
    │   │   ├── request.py      # Pydantic request models
    │   │   └── response.py     # Pydantic response models
    │   └── routes/
    │       ├── chat.py         # /chat endpoints
    │       ├── admin.py        # /admin endpoints
    │       ├── users.py        # /auth endpoints
    │       ├── conversations.py# /conversations endpoints
    │       └── health.py       # /health endpoint
    ├── auth/
    │   └── __init__.py         # JWT creation/verification, email utils
    ├── core/
    │   ├── config.py           # ChatbotConfig dataclass
    │   ├── logging_config.py   # Rotating file logger setup
    │   └── exceptions.py       # Custom exception classes
    ├── postgresql_db/
    │   ├── database.py         # SQLModel engine, session, init_db
    │   └── models.py           # User, Conversation, Message models
    ├── prompts/
    │   └── medical_prompts.py  # LangChain PromptTemplate for medical Q&A
    ├── services/
    │   ├── rag_service.py      # ConversationalRetrievalChain setup
    │   ├── embedding_service.py# Embedding model initialization
    │   ├── vectorstore_service.py # ChromaDB initialization
    │   ├── memory_service.py   # Per-session memory manager
    │   └── document_service.py # PDF loading and text splitting
    ├── validators/
    │   └── safety.py           # Query safety validation
    └── analyzers/
        └── response_analyzer.py# Response confidence scoring
```

---

## ✅ Prerequisites

- **Python 3.10+**
- **PostgreSQL 14+**
- **[Ollama](https://ollama.com/)** installed and running

Pull the required models:
```bash
ollama pull llama3.2:1b
ollama pull nomic-embed-text
```

---

## 📦 Installation

```bash
# From the project root
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

---

## ⚙️ Configuration

All configuration lives in `src/core/config.py` as a `ChatbotConfig` dataclass.

| Setting | Default | Description |
|---|---|---|
| `LLM_MODEL` | `llama3.2:1b` | Ollama model name |
| `EMBEDDING_MODEL` | `nomic-embed-text` | Embedding model |
| `TEMPERATURE` | `0.5` | LLM temperature |
| `MEMORY_WINDOW_SIZE` | `4` | Q&A pairs kept in memory |
| `CHUNK_SIZE` | `1000` | PDF chunk size (chars) |
| `CHUNK_OVERLAP` | `400` | Chunk overlap (chars) |
| `RETRIEVAL_K` | `5` | Top-K documents retrieved |
| `SEARCH_TYPE` | `similarity` | ChromaDB search type |
| `ENABLE_MEDICAL_DISCLAIMER` | `True` | Append disclaimer to responses |
| `ENABLE_EMERGENCY_DETECTION` | `True` | Detect emergency queries |

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/medical_db

# JWT
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com

# Frontend URL (for email redirect links)
FRONTEND_URL=http://localhost:5173
```

---

## 🗄️ Database Setup

Run the provided setup script to create the PostgreSQL database:

```bash
chmod +x setup_database.sh
./setup_database.sh
```

This will:
1. Create the `medical_db` database
2. Grant privileges to the `postgres` user
3. Generate a `.env` file with a random `SECRET_KEY`

Tables are created automatically on first server startup via SQLModel's `init_db()`.

**Database Models:**
- `User` — email, full_name, password_hash, is_verified, verification_token
- `Conversation` — title, user_id, created_at
- `Message` — conversation_id, role (user/assistant), content, query_type, elapsed_time, docs_retrieved

---

## 📄 Adding Medical Documents

Place your PDF files in the `backend/data/` directory:

```bash
mkdir -p data
cp /path/to/your/medical_document.pdf data/
```

The vector database is built automatically on first startup (if `db/` doesn't exist). To rebuild manually, call the admin endpoint:

```bash
curl -X POST "http://localhost:8000/admin/rebuild-db?confirm=true" \
  -H "Authorization: Bearer <your_token>"
```

---

## ▶️ Running the Server

```bash
# From the backend/ directory, with venv activated
python main.py
```

Or with Uvicorn directly:
```bash
uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
```

The server starts on **`http://localhost:8000`**

| URL | Description |
|---|---|
| `http://localhost:8000/docs` | Swagger UI (interactive API docs) |
| `http://localhost:8000/redoc` | ReDoc documentation |
| `http://localhost:8000/health` | Health check endpoint |

---

## 📡 API Reference

### Authentication (`/auth`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/auth/register` | ❌ | Register new user |
| `POST` | `/auth/login` | ❌ | Login (returns JWT) |
| `GET` | `/auth/verify/{token}` | ❌ | Verify email |
| `POST` | `/auth/forgot-password` | ❌ | Request password reset |
| `POST` | `/auth/reset-password` | ❌ | Reset password with token |
| `GET` | `/auth/me` | ✅ | Get current user |
| `POST` | `/auth/logout` | ✅ | Logout (client-side token removal) |

### Chat (`/chat`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/chat` | ✅ | Send message, get AI response |
| `GET` | `/chat/history` | ✅ | Get conversation history |
| `POST` | `/chat/reset` | ✅ | Clear conversation memory |
| `POST` | `/chat/export` | ✅ | Export conversation (JSON/TXT) |
| `GET` | `/chat/status` | ❌ | Chat service status |

**Example Chat Request:**
```json
POST /chat
{
  "message": "What are the symptoms of diabetes?",
  "conversation_id": 1,
  "response_type": "detailed"
}
```

**Example Chat Response:**
```json
{
  "status": "success",
  "response": "Diabetes symptoms include...",
  "conversation_id": 1,
  "confidence": "high",
  "confidence_score": 0.87,
  "response_time": 2.34,
  "sources": [...],
  "disclaimer": "This is for informational purposes only...",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Conversations (`/conversations`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/conversations` | ✅ | List all conversations |
| `GET` | `/conversations/{id}` | ✅ | Get conversation with messages |
| `DELETE` | `/conversations/{id}` | ✅ | Delete conversation |

### Admin (`/admin`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/admin/metrics` | Performance metrics |
| `POST` | `/admin/metrics/reset` | Reset metrics |
| `GET` | `/admin/metrics/export` | Export metrics |
| `POST` | `/admin/clear-db` | Clear vector database |
| `POST` | `/admin/rebuild-db` | Rebuild vector database |
| `GET` | `/admin/database/info` | Vector DB info |
| `POST` | `/admin/memory/clear` | Clear all session memory |
| `GET` | `/admin/logs` | View recent logs |

---

## 🔄 RAG Pipeline

1. **Document Loading** — PDFs in `data/` are loaded with `PyPDFLoader`
2. **Text Splitting** — Documents split into 1000-char chunks with 400-char overlap
3. **Embedding** — Chunks embedded using `nomic-embed-text`
4. **Vector Store** — Embeddings stored in ChromaDB (persisted to `db/`)
5. **Retrieval** — Top-5 most similar chunks retrieved for each query
6. **Generation** — `llama3.2:1b` generates answer using retrieved context + conversation history
7. **Memory** — Last 4 Q&A pairs kept in `ConversationBufferWindowMemory` per session

---

## 🔐 Authentication Flow

```
Register → Email Verification → Login → JWT Token → Protected Routes
              ↑
         (SMTP email with verification link)

Forgot Password → Reset Email → Reset Password Link → New Password
```

- Tokens are **JWT** (HS256), expire after 24 hours by default
- Passwords are hashed with **bcrypt**
- Email verification is **required** before login
- Password reset uses a one-time token stored in the database

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test files
pytest src/api/test_api.py
pytest src/services/test_services.py
pytest src/core/test_core.py
pytest src/validators/test_validators.py

# Run with verbose output
pytest -v

# Verify API is running correctly
python verify_api.py
```

---

## 📝 Logging

Logs are written to `logs/chatbot_YYYYMMDD.log` (daily rotation).

Log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

View recent logs via the admin endpoint:
```bash
curl "http://localhost:8000/admin/logs?lines=100&level=ERROR"
```
