# 🏥 Medical Chatbot

An AI-powered medical information chatbot built with a **FastAPI** backend and a **React + TypeScript** frontend. It uses **Retrieval-Augmented Generation (RAG)** with **Ollama** (local LLM) and **ChromaDB** (vector store) to answer medical questions from indexed PDF documents, with full user authentication, conversation history, and a modern chat UI.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Getting Started](#-getting-started)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Backend Setup](#2-backend-setup)
  - [3. Frontend Setup](#3-frontend-setup)
- [Environment Variables](#-environment-variables)
- [Running the Application](#-running-the-application)
- [API Overview](#-api-overview)
- [Screenshots](#-screenshots)
- [License](#-license)

---

## ✨ Features

- 🤖 **AI-Powered Q&A** — Answers medical questions using a local LLM (Llama 3.2) via Ollama
- 📄 **RAG Pipeline** — Retrieves relevant context from indexed PDF medical documents using ChromaDB
- 💬 **Conversation Memory** — Maintains per-session chat history for follow-up questions
- 🔐 **JWT Authentication** — Secure user registration, login, email verification, and password reset
- 📧 **Email Notifications** — Sends verification and password-reset emails via SMTP
- 🗂️ **Conversation Management** — Create, browse, and delete past conversations
- 🛡️ **Safety Validation** — Detects emergency situations, harmful queries, and adds medical disclaimers
- 📊 **Admin Panel** — Performance metrics, log viewer, vector DB management via API
- 🌗 **Dark / Light Mode** — System-aware theme with manual toggle
- 📱 **Responsive UI** — Works on desktop and mobile

---

## 🛠️ Tech Stack

### Backend
| Layer | Technology |
|---|---|
| API Framework | FastAPI + Uvicorn |
| LLM | Ollama (`llama3.2:3b`) |
| Embeddings | `nomic-embed-text` via Ollama / HuggingFace |
| RAG Orchestration | LangChain |
| Vector Store | ChromaDB |
| Database | PostgreSQL + SQLModel + Alembic |
| Auth | JWT (`python-jose`) + Bcrypt |
| PDF Parsing | PyPDF |
| Testing | Pytest + HTTPX |

### Frontend
| Layer | Technology |
|---|---|
| Framework | React 19 + TypeScript |
| Build Tool | Vite |
| Styling | Tailwind CSS + shadcn/ui (Radix UI) |
| Routing | React Router v7 |
| Animations | Framer Motion |
| Markdown Rendering | react-markdown |
| State / Auth | React Context API |

---

## 📁 Project Structure

```
MedicalChatbot/
├── backend/                    # FastAPI backend
│   ├── main.py                 # Server entry point
│   ├── requirements.txt        # Python dependencies (root-level)
│   ├── setup_database.sh       # PostgreSQL setup script
│   ├── setup_api.sh            # API setup helper script
│   ├── verify_api.py           # API verification script
│   ├── data/                   # PDF medical documents (place here)
│   ├── db/                     # ChromaDB vector store (auto-generated)
│   ├── logs/                   # Application logs (auto-generated)
│   └── src/
│       ├── api/                # FastAPI app, routes, middleware, models
│       │   ├── routes/         # chat, admin, auth, conversations, health
│       │   └── models/         # Request/Response Pydantic models
│       ├── auth/               # JWT auth, email utilities
│       ├── core/               # Config, logging, exceptions
│       ├── postgresql_db/      # SQLModel DB models and session
│       ├── prompts/            # LangChain prompt templates
│       ├── services/           # RAG, embedding, vector store, memory
│       ├── validators/         # Safety and query validators
│       └── analyzers/          # Response confidence analyzers
│
├── frontend/                   # React + TypeScript frontend
│   ├── index.html
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── src/
│       ├── App.tsx             # Root app with routing
│       ├── components/
│       │   ├── auth/           # Login, Register, ForgotPassword dialogs
│       │   ├── chat/           # ChatInterface, ChatSidebar, ChatMessage, etc.
│       │   └── ui/             # shadcn/ui component library
│       ├── context/            # AuthContext (JWT state management)
│       ├── hooks/              # Custom React hooks
│       ├── pages/              # VerifyEmail, ResetPassword pages
│       └── services/           # API service layer (axios/fetch wrappers)
│
├── requirements.txt            # Python dependencies
├── .env                        # Root-level env (optional)
└── .gitignore
```

---

## ✅ Prerequisites

Make sure the following are installed on your system:

- **Python 3.10+**
- **Node.js 18+** and **npm**
- **PostgreSQL 14+**
- **[Ollama](https://ollama.com/)** — for running the local LLM

Pull the required Ollama models:
```bash
ollama pull llama3.2:1b
ollama pull nomic-embed-text
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/tuhin1522/MedicalChatbot.git
cd MedicalChatbot
```

### 2. Backend Setup

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Set up PostgreSQL database
cd backend
chmod +x setup_database.sh
./setup_database.sh

# Configure environment variables (see .env section below)
cp .env.example .env           # Edit with your values

# Add your medical PDF documents
mkdir -p data
# Copy your PDF files into backend/data/
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

---

## 🔑 Environment Variables

Create a `.env` file inside the `backend/` directory:

```env
# Database
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/medical_db

# JWT Security
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Email (SMTP) — required for email verification & password reset
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com

# Frontend URL (for email redirect links)
FRONTEND_URL=http://localhost:5173
```

> **Tip:** Use a Gmail App Password (not your regular password) for `SMTP_PASSWORD`.

---

## ▶️ Running the Application

### Start the Backend

```bash
# From the project root, with venv activated
cd backend
python main.py
```

The API will be available at:
- **API Base:** `http://localhost:8000`
- **Swagger Docs:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Start the Frontend

```bash
cd frontend
npm run dev
```

The frontend will be available at: **`http://localhost:5173`**

---

## 📡 API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API info |
| `GET` | `/health` | Health check |
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login and get JWT token |
| `GET` | `/auth/verify/{token}` | Verify email address |
| `POST` | `/auth/forgot-password` | Request password reset |
| `POST` | `/auth/reset-password` | Reset password with token |
| `GET` | `/auth/me` | Get current user profile |
| `POST` | `/chat` | Send a message and get AI response |
| `GET` | `/chat/history` | Get conversation history |
| `POST` | `/chat/reset` | Reset conversation memory |
| `POST` | `/chat/export` | Export conversation (JSON/TXT) |
| `GET` | `/conversations` | List all conversations |
| `DELETE` | `/conversations/{id}` | Delete a conversation |
| `GET` | `/admin/metrics` | Performance metrics |
| `POST` | `/admin/rebuild-db` | Rebuild vector database |
| `GET` | `/admin/logs` | View recent logs |

Full interactive documentation is available at `/docs` when the server is running.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> ⚠️ **Disclaimer:** This chatbot is for **informational purposes only** and does **not** constitute medical advice. Always consult a qualified healthcare professional for medical decisions.
