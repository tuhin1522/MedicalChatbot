# Medical Chatbot 🩺🤖

A professional, full-stack RAG-based (Retrieval-Augmented Generation) medical chatbot with a modern React frontend and FastAPI backend. Provides context-aware answers to medical queries by extracting information from trusted medical documents.

## 🚀 Features

### Backend
- **PDF Data Extraction**: Automatically loads and processes medical literature from the `data/` directory
- **Efficient Retrieval**: Uses **ChromaDB** for fast vector search and retrieval
- **State-of-the-Art LLM**: Powered by **Google Gemini Flash** for accurate and concise responses
- **Source Referencing**: Keeps track of original document sources for transparency
- **RESTful API**: Clean API endpoints for frontend integration

### Frontend
- **Modern UI/UX**: Built with React 19 + Vite + Tailwind CSS
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Real-time Chat**: Smooth animations and typing indicators
- **Quick Actions**: Pre-defined medical questions for quick access
- **Beautiful Gradients**: Premium design with glassmorphism effects

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Orchestration**: LangChain
- **LLM**: Google Generative AI (Gemini Flash)
- **Vector Database**: ChromaDB
- **Embeddings**: HuggingFace (sentence-transformers)

### Frontend
- **Framework**: React 19
- **Build Tool**: Vite 7
- **Styling**: Tailwind CSS v4
- **Fonts**: Google Fonts (Inter)
- **HTTP Client**: Fetch API

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Google Gemini API Key

## ⚙️ Quick Start

### Option 1: Automated Setup (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tuhin1522/MedicalChatbot.git
   cd MedicalChatbot
   ```

2. **Set up environment variables:**
   ```bash
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

3. **Make start script executable and run:**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

This will automatically:
- Create and activate a virtual environment
- Install all Python dependencies
- Install all Node.js dependencies
- Start both backend and frontend servers

### Option 2: Manual Setup

1. **Clone and configure:**
   ```bash
   git clone https://github.com/tuhin1522/MedicalChatbot.git
   cd MedicalChatbot
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

2. **Backend setup:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cd backend
   python3 app.py
   ```

3. **Frontend setup (in a new terminal):**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 📂 Project Structure

```text
MedicalChatbot/
├── backend/
│   ├── app.py              # Flask API server
│   ├── src/
│   │   ├── helper.py       # PDF loading & embeddings
│   │   └── prompt.py       # AI prompt templates
│   ├── data/               # Source PDF documents
│   ├── db/                 # ChromaDB vector store
│   └── store_index.py      # Vector DB creation script
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── ChatHeader.jsx
│   │   │   ├── ChatMessage.jsx
│   │   │   └── ChatInput.jsx
│   │   ├── App.jsx         # Root component
│   │   ├── App.css         # Custom animations
│   │   └── index.css       # Global styles
│   ├── public/             # Static assets
│   └── package.json        # Node dependencies
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🏃 Running the Application

### Start Servers
```bash
./start.sh
```

### Stop Servers
```bash
./stop.sh
```

### Access the Application
- **Frontend**: http://localhost:5173 (or next available port)
- **Backend API**: http://localhost:8080

## 📚 Initial Data Setup

1. **Add medical documents:**
   Place your medical PDF files in the `backend/data/` directory.

2. **Create vector database:**
   ```bash
   cd backend
   python store_index.py
   ```

This indexes your documents for efficient retrieval.

## 🎨 UI Features

- **Welcome Screen**: Friendly introduction when no messages exist
- **Message Bubbles**: Distinct styling for user and bot messages
- **Avatars**: Icon-based avatars with gradient backgrounds
- **Typing Indicator**: Animated dots while bot is thinking
- **Quick Actions**: One-click buttons for common medical questions
- **Timestamps**: Message time for each conversation
- **Auto-scroll**: Automatically scrolls to newest messages

## 🔧 Configuration

### Backend Port
Edit `backend/app.py`:
```python
app.run(host="0.0.0.0", port=8080, debug=True)
```

### Frontend Port
Edit `frontend/vite.config.js`:
```javascript
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: { port: 3000 }
})
```

### AI Model
Edit `backend/app.py`:
```python
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0.4)
```

## 🚀 Deployment

### Frontend (Static Build)
```bash
cd frontend
npm run build
# Deploy the 'dist' folder to any static hosting service
```

### Backend (Production)
```bash
pip install gunicorn
cd backend
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

## 📖 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Comprehensive setup and troubleshooting guide
- **[frontend/README.md](frontend/README.md)** - Frontend-specific documentation

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
