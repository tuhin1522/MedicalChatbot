#!/bin/bash

# Medical Chatbot API Setup Script
# Quick start guide for running the API server

set -e  # Exit on error

echo "🏥 Medical Chatbot API Setup"
echo "======================================"

# Check Python version
echo ""
echo "📋 Checking Python version..."
python3 --version

# Check if in correct directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this script from the backend directory."
    exit 1
fi

# Check Ollama installation
echo ""
echo "📋 Checking Ollama installation..."
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not found. Please install from: https://ollama.ai"
    echo "   Continue anyway? (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        exit 1
    fi
else
    echo "✅ Ollama installed"
    
    # Check required models
    echo ""
    echo "📋 Checking Ollama models..."
    if ollama list | grep -q "llama3.2:1b"; then
        echo "✅ llama3.2:1b found"
    else
        echo "⚠️  llama3.2:1b not found"
        echo "   Install with: ollama pull llama3.2:1b"
    fi
    
    if ollama list | grep -q "nomic-embed-text"; then
        echo "✅ nomic-embed-text found"
    else
        echo "⚠️  nomic-embed-text not found"
        echo "   Install with: ollama pull nomic-embed-text"
    fi
fi

# Check dependencies
echo ""
echo "📋 Checking Python dependencies..."
if python3 -c "import fastapi" 2>/dev/null; then
    echo "✅ FastAPI installed"
else
    echo "⚠️  FastAPI not installed"
    echo "   Installing dependencies..."
    pip3 install --user -r requirements.txt
fi

# Check vector database
echo ""
echo "📋 Checking vector database..."
if [ -d "db" ]; then
    echo "✅ Vector database found"
else
    echo "⚠️  Vector database not found"
    echo "   Create it with: python3 store_index.py"
fi

# Summary
echo ""
echo "======================================"
echo "📊 Setup Summary"
echo "======================================"
echo ""
echo "To start the API server:"
echo "  python3 main.py"
echo ""
echo "To create the vector database (if missing):"
echo "  python3 store_index.py"
echo ""
echo "To test the API:"
echo "  python3 example_client.py"
echo ""
echo "API Documentation (after starting server):"
echo "  http://localhost:8000/docs"
echo ""
echo "======================================"
