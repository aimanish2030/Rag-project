# RAG Project — PDF Question Answering API

A Basic RAG (Retrieval-Augmented Generation) system built with LangChain, Groq, ChromaDB, and FastAPI.

## What does this do?

Upload any PDF → Ask questions → Get answers from the PDF content

## Tech Stack

- **LangChain** — RAG pipeline
- **Groq (LLaMA 3.1)** — LLM for generating answers
- **ChromaDB** — Vector database for storing embeddings
- **HuggingFace Embeddings** — Converting text to vectors
- **FastAPI** — REST API

## Project Structure

```
rag_project/
├── main.py        # FastAPI endpoints
├── rag.py         # RAG logic
├── requirements.txt
├── .env           # API keys (not uploaded)
└── .gitignore
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/aimanish2030/Rag-project.git
cd Rag-project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env` file

```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key from: https://console.groq.com

### 4. Run the server

```bash
uvicorn main:app --reload
```

### 5. Open API docs

```
http://127.0.0.1:8000/docs
```

## API Endpoints

### POST `/upload`
Upload a PDF file to process.

**Request:** `multipart/form-data` with PDF file

**Response:**
```json
{
  "message": "PDF successfully process ho gayi",
  "filename": "example.pdf",
  "total_chunks": 60
}
```

### POST `/ask`
Ask a question about the uploaded PDF.

**Request:**
```json
{
  "question": "What topics are covered in this PDF?"
}
```

**Response:**
```json
{
  "question": "What topics are covered in this PDF?",
  "answer": "The PDF covers..."
}
```

### GET `/`
Health check — confirms API is running.

## How it works

```
PDF Upload
    ↓
PyPDFLoader reads the PDF
    ↓
Text split into chunks (500 chars each)
    ↓
HuggingFace Embeddings converts chunks to vectors
    ↓
Vectors saved in ChromaDB

User asks a question
    ↓
Question converted to vector
    ↓
Top 3 similar chunks found in ChromaDB
    ↓
Chunks + Question sent to Groq LLaMA 3.1
    ↓
Answer returned to user
```

## Note

- Only text-based PDFs work (not scanned/image PDFs)
- Make sure `.env` file is created before running