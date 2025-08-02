# rag_logic.py
import pdfplumber
import faiss
from sentence_transformers import SentenceTransformer
import os


EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
EMBED_DIM = 384
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
    global index, doc_store
    vectors = EMBED_MODEL.encode(chunks)
    index.add(vectors)
    for i, chunk in enumerate(chunks):
        doc_store[len(doc_store)] = chunk

def retrieve_chunks(query, k=5):
    query_vec = EMBED_MODEL.encode([query])
    D, I = index.search(query_vec, k)
    return [doc_store[i] for i in I[0] if i in doc_store]
