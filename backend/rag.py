# rag_logic.py
import pdfplumber
import faiss
import google.generativeai as genai
import os
import numpy as np


genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
EMBED_MODEL = "models/embedding-001"
EMBED_DIM = 768
index = faiss.IndexFlatL2(EMBED_DIM)
doc_store = {} 

def reset_storage():
    global index, doc_store
    print(" Deleting old embeddings and documents...")
    index = faiss.IndexFlatL2(EMBED_DIM)
    doc_store = {}


def extract_pdf_text(file_path):
    full_text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    return full_text.strip()

def chunk_text(text, chunk_size=500):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def embed_and_store(chunks):

    reset_storage()

    global index, doc_store

    response = genai.embed_content(
        model=EMBED_MODEL,
        content=chunks,
        task_type="RETRIEVAL_DOCUMENT"
    )
    vectors = response['embedding']
    
    index.add(np.array(vectors, dtype=np.float32))
    
    for i, chunk in enumerate(chunks):
        doc_store[len(doc_store)] = chunk

def retrieve_chunks(query, k=5):
   
    response = genai.embed_content(
        model=EMBED_MODEL,
        content=query,
        task_type="RETRIEVAL_QUERY"
    )
    query_vec = response['embedding']
    D, I = index.search(np.array([query_vec], dtype=np.float32), k)
    return [doc_store[i] for i in I[0] if i in doc_store]
