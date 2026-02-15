from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..core import config, logger

# Extract text from PDF files in the 'data' directory
def load_pdf(data):
    loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    Given a list of Document objects, return a new list of Document objects
    containing only 'source' in metadata and the original page_content.
    """
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    return minimal_docs

def text_split(minimal_documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE, 
        chunk_overlap=config.CHUNK_OVERLAP
    )
    text_chunks = text_splitter.split_documents(minimal_documents)
    return text_chunks
