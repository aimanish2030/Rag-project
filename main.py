import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import process_pdf, ask_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class QuestionRequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Sirf PDF upload karo")
    
    file_path = f"{UPLOAD_FOLDER}/{file.filename}"
    
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    total_chunks = process_pdf(file_path)
    
    return {
        "message": "PDF successfully process ho gayi",
        "filename": file.filename,
        "total_chunks": total_chunks
    }

@app.post("/ask")
async def ask(request: QuestionRequest):
    if not os.path.exists("./chroma_db"):
        raise HTTPException(status_code=400, detail="Pehle PDF upload karo")
    
    answer = ask_question(request.question)
    
    return {
        "question": request.question,
        "answer": answer
    }

@app.get("/")
async def root():
    return {"message": "RAG API chal rahi hai!"}