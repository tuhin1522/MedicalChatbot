from src.helper import load_pdf, text_split, download_hugging_face_embeddings, filter_to_minimal_docs
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv

load_dotenv()

# Load and process the documents
extracted_data = load_pdf("data/")
# Filter metadata to keep ONLY 'source'
text_chunks = filter_to_minimal_docs(extracted_data)
text_chunks = text_split(text_chunks)
embeddings = download_hugging_face_embeddings()

# Initialize ChromaDB
persist_directory = "db"

# Create the vector store and persist it
vectordb = Chroma.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    persist_directory=persist_directory
)

print("Vector store created and persisted in:", persist_directory)
