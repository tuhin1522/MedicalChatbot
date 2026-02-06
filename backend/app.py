from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from src.helper import download_hugging_face_embeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import uvicorn
import os
from src.prompt import *

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Medical Chatbot API",
    description="AI-powered medical chatbot using RAG and Google Gemini",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize embeddings and vector database
embeddings = download_hugging_face_embeddings()
persist_directory = "db"

# Load the existing vector store
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

# Set up prompt template
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs = {"prompt": PROMPT}

# Using Gemini
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0.4)

# Create QA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Medical Chatbot API",
        "version": "2.0.0",
        "status": "online",
        "endpoints": {
            "/": "API information",
            "/get": "POST - Send a medical question",
            "/health": "GET - Health check",
            "/docs": "API documentation (Swagger UI)"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Medical Chatbot API"}


@app.post("/get", response_class=PlainTextResponse)
async def chat(msg: str = Form(...)):
    """
    Process user message and return AI response
    
    Args:
        msg: User's medical question
        
    Returns:
        AI-generated response based on medical documents
    """
    if not msg or not msg.strip():
        raise HTTPException(status_code=400, detail="Please enter a message.")
    
    msg = msg.strip()
    print(f"User Question: {msg}")
    
    try:
        # Using .invoke() as per latest LangChain standards
        result = qa.invoke({"query": msg})
        response = result.get("result", "I'm sorry, I couldn't find an answer for that.")
        
        print(f"Chatbot Response: {response}")
        return response
    
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request."
        )


if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
