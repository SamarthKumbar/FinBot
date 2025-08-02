from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import auth,balance


app = FastAPI()

app.include_router(auth.auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(balance.router, prefix="/rag", tags=["RAG"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running 🚀"}
