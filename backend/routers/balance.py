# rag_routes.py
import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from backend.rag import extract_pdf_text, chunk_text, embed_and_store, retrieve_chunks
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

class QueryRequest(BaseModel):
    query: str

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        text = extract_pdf_text(tmp_path)
    finally:
        os.remove(tmp_path)

    if not text:
        raise HTTPException(status_code=400, detail="No text extracted from PDF.")

    chunks = chunk_text(text)
    embed_and_store(chunks)
    return {"message": f"Uploaded and embedded {len(chunks)} chunks."}

@router.post("/ask")
async def ask_question(request: QueryRequest):
    chunks = retrieve_chunks(request.query)
    context = "\n\n".join(chunks)

    prompt = f"""You are a financial analyst AI. Based on the below balance sheet context, answer the question.

Context:
{context}

Question: {request.query}
Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"answer": response.choices[0].message.content}
