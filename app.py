from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from src.prompt import *

app = Flask(__name__)

load_dotenv()

embeddings = download_hugging_face_embeddings()
persist_directory = "db"

# Load the existing vector store
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs = {"prompt": PROMPT}

# Using Gemini instead of OpenAI
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0.4)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form.get("msg", "").strip()
    if not msg:
        return "Please enter a message."
    
    print(f"User Question: {msg}")
    
    # Using .invoke() as per latest LangChain standards
    result = qa.invoke({"query": msg})
    response = result.get("result", "I'm sorry, I couldn't find an answer for that.")
    
    print(f"Chatbot Response: {response}")
    return str(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)
