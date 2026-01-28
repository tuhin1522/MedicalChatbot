# Medical Chatbot 🩺🤖

A professional, RAG-based (Retrieval-Augmented Generation) medical chatbot designed to provide context-aware answers to medical queries by extracting information from trusted medical documents (PDFs).

## 🚀 Features
- **PDF Data Extraction**: Automatically loads and processes medical literature from the `data/` directory.
- **Efficient Retrieval**: Uses **ChromaDB** for fast vector search and retrieval.
- **State-of-the-Art LLM**: Powered by **Google Gemini Pro (Flash)** for accurate and concise responses.
- **Modern UI**: A sleek, responsive chat interface with a professional medical aesthetic and custom avatars.
- **Source Referencing**: Keeps track of original document sources for transparency.

## 🛠️ Tech Stack
- **Framework**: Flask
- **Orchestration**: LangChain
- **LLM**: Google Generative AI (Gemini)
- **Vector Database**: ChromaDB
- **Embeddings**: HuggingFace (sentence-transformers)
- **Frontend**: HTML5, CSS3, Bootstrap, jQuery

## 📋 Prerequisites
- Python 3.10 or higher
- Google Gemini API Key

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tuhin1522/MedicalChatbot.git
   cd MedicalChatbot
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your Google API key:
   ```env
   GOOGLE_API_KEY=YOUR_GEMINI_API_KEY_HERE
   ```

5. **Prepare Medical Data:**
   Place your medical PDF documents inside the `data/` folder.

6. **Index the Documents:**
   Run the indexing script to populate the vector database:
   ```bash
   python store_index.py
   ```

## 🏃 Running the Application
Start the Flask server:
```bash
python app.py
```
The application will be available at `http://localhost:8080`.

## 📂 Project Structure
```text
MedicalChatbot/
├── data/               # Source PDF documents
├── db/                 # ChromaDB persistent storage
├── research/           # Jupyter notebooks for experiments
├── src/                # Backend utility functions
│   ├── helper.py       # PDF loading & text splitting
│   └── prompt.py       # System prompt templates
├── static/             # CSS & custom image assets
├── templates/          # HTML chat interface
├── app.py              # Main Flask application
├── store_index.py      # Script to create vector store
└── requirements.txt    # Project dependencies
```

## 🎨 UI Preview
The chatbot features a premium design with custom medical avatars:
- **Chatbot Avatar**: A friendly robot with healthcare symbols.
- **User Avatar**: Professional minimalist silhouette.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
