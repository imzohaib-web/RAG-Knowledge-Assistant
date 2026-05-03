"""
RAG Knowledge Assistant Backend
FastAPI application for PDF processing, embeddings, and chat functionality
"""

import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.pdf_processor import PDFProcessor
from services.text_chunker import TextChunker
from services.embedding_service import EmbeddingService
from services.vector_store import VectorStore
from services.llm_service import LLMService

# Initialize FastAPI app
app = FastAPI(title="RAG Knowledge Assistant", version="1.0.0")

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
pdf_processor = PDFProcessor()
text_chunker = TextChunker()
embedding_service = EmbeddingService()
vector_store = VectorStore()
llm_service = LLMService()

# Data models
class ChatRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None
    top_k: Optional[int] = 3
    model: Optional[str] = None
    temperature: Optional[float] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    source_chunks: List[Dict[str, Any]]
    model_used: Optional[str] = None
    chunks_used: int = 0

class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_created: int
    total_pages: int

class HistoryEntry(BaseModel):
    conversation_id: str
    question: str
    answer: str
    source_pages: List[str]
    timestamp: str

class FeedbackEntry(BaseModel):
    conversation_id: str
    message_id: str
    rating: str
    question: Optional[str] = None
    answer: Optional[str] = None
    timestamp: Optional[str] = None

class SettingsRequest(BaseModel):
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 3
    model: str = "llama3-70b-8192"
    temperature: float = 0.3

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("vector_store", exist_ok=True)
HISTORY_FILE = "history.json"
FEEDBACK_FILE = "feedback.json"
SETTINGS_FILE = "settings.json"

current_pdf_info = {
    "filename": None,
    "chunks_created": 0,
    "total_pages": 0,
}


def _read_json_file(path: str, default: Any):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def _write_json_file(path: str, data: Any):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def _load_settings() -> Dict[str, Any]:
    default_settings = {
        "chunk_size": 500,
        "chunk_overlap": 50,
        "top_k": 3,
        "model": "llama3-70b-8192",
        "temperature": 0.3,
    }
    loaded = _read_json_file(SETTINGS_FILE, default_settings)
    for key, value in default_settings.items():
        loaded.setdefault(key, value)
    return loaded

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "RAG Knowledge Assistant API is running"}


@app.get("/settings")
async def get_settings():
    return _load_settings()


@app.post("/settings")
async def update_settings(settings: SettingsRequest):
    safe_settings = {
        "chunk_size": max(200, min(1000, settings.chunk_size)),
        "chunk_overlap": max(0, min(200, settings.chunk_overlap)),
        "top_k": max(1, min(10, settings.top_k)),
        "model": settings.model,
        "temperature": max(0.0, min(1.0, settings.temperature)),
    }
    _write_json_file(SETTINGS_FILE, safe_settings)
    text_chunker.set_chunking(
        safe_settings["chunk_size"],
        safe_settings["chunk_overlap"]
    )
    return {"message": "Settings saved successfully", "settings": safe_settings}

@app.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and process a PDF file
    - Extract text using pdfplumber
    - Chunk the text with LangChain
    - Create embeddings with HuggingFace
    - Store in FAISS vector database
    """
    file_path = None
    try:
        # Validate file type
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Save uploaded file
        file_id = str(uuid.uuid4())
        safe_filename = os.path.basename(file.filename)
        file_path = f"uploads/{file_id}_{safe_filename}"
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Extract text from PDF
        extracted_text = pdf_processor.extract_text(file_path)
        if not extracted_text:
            raise HTTPException(
                status_code=400,
                detail="No readable text found in this PDF. Try a text-based PDF."
            )
        
        # Rebuild vector store for new PDF upload
        vector_store.clear_store()

        # Apply current settings for chunking
        settings = _load_settings()
        text_chunker.set_chunking(
            settings.get("chunk_size", 500),
            settings.get("chunk_overlap", 50)
        )

        # Chunk the text
        chunks = text_chunker.chunk_text(extracted_text)
        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Failed to create text chunks from the uploaded PDF."
            )
        
        total_pages = len(extracted_text)

        # Create embeddings for chunks
        chunk_texts = [chunk["text"] for chunk in chunks]
        embeddings = embedding_service.create_embeddings(chunk_texts)
        if len(embeddings) == 0:
            raise HTTPException(
                status_code=400,
                detail="Failed to generate embeddings from extracted PDF content."
            )
        
        # Store in vector database
        vector_store.store_chunks(chunks, embeddings)
        
        current_pdf_info["filename"] = file.filename
        current_pdf_info["chunks_created"] = len(chunks)
        current_pdf_info["total_pages"] = total_pages

        return UploadResponse(
            message=f"PDF processed: {len(chunks)} chunks created",
            filename=file.filename,
            chunks_created=len(chunks),
            total_pages=total_pages
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for asking questions about uploaded documents
    - Convert question to embedding
    - Search FAISS for relevant chunks
    - Send to Groq LLM for answer
    """
    try:
        # Check if vector store has any data
        if not vector_store.has_data():
            raise HTTPException(status_code=400, detail="No documents uploaded yet")
        
        settings = _load_settings()
        top_k = max(1, min(10, request.top_k if request.top_k is not None else settings.get("top_k", 3)))
        model = request.model or settings.get("model")
        temperature = request.temperature if request.temperature is not None else settings.get("temperature", 0.3)

        # Create embedding for the question
        question_embedding = embedding_service.create_embeddings([request.question])[0]
        
        # Search for relevant chunks
        relevant_chunks = vector_store.search(question_embedding, top_k=top_k)
        
        # Generate answer using LLM
        llm_response = llm_service.generate_answer(
            request.question,
            relevant_chunks,
            model=model,
            temperature=temperature
        )
        answer = llm_response.get("answer", "")
        model_used = llm_response.get("model_used")
        
        # Extract source page numbers
        sources = [f"Page {chunk['page_number']}" for chunk in relevant_chunks]
        unique_sources = list(set(sources))

        # Persist Q&A history
        conversation_id = request.conversation_id or str(uuid.uuid4())
        history_entry = {
            "conversation_id": conversation_id,
            "question": request.question,
            "answer": answer,
            "source_pages": unique_sources,
            "timestamp": datetime.utcnow().isoformat()
        }
        history_data = _read_json_file(HISTORY_FILE, [])
        history_data.append(history_entry)
        _write_json_file(HISTORY_FILE, history_data)
        
        return ChatResponse(
            answer=answer,
            sources=unique_sources,
            source_chunks=relevant_chunks,
            model_used=model_used,
            chunks_used=len(relevant_chunks)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@app.post("/history", response_model=Dict[str, Any])
async def save_history(entry: HistoryEntry):
    history_data = _read_json_file(HISTORY_FILE, [])
    history_data.append(entry.model_dump())
    _write_json_file(HISTORY_FILE, history_data)
    return {"message": "History saved successfully"}


@app.get("/history/get", response_model=List[Dict[str, Any]])
async def get_history():
    return _read_json_file(HISTORY_FILE, [])


@app.delete("/history/delete/{conversation_id}")
async def delete_history(conversation_id: str):
    history_data = _read_json_file(HISTORY_FILE, [])
    filtered = [item for item in history_data if item.get("conversation_id") != conversation_id]
    _write_json_file(HISTORY_FILE, filtered)
    return {"message": "Conversation deleted successfully"}


@app.post("/feedback")
async def save_feedback(entry: FeedbackEntry):
    payload = entry.model_dump()
    if not payload.get("timestamp"):
        payload["timestamp"] = datetime.utcnow().isoformat()
    feedback_data = _read_json_file(FEEDBACK_FILE, [])
    feedback_data.append(payload)
    _write_json_file(FEEDBACK_FILE, feedback_data)
    return {"message": "Feedback saved successfully"}


@app.get("/pdf-info")
async def get_pdf_info():
    return current_pdf_info


@app.delete("/clear")
async def clear_data():
    """Clear all stored documents and embeddings"""
    try:
        vector_store.clear_store()
        current_pdf_info["filename"] = None
        current_pdf_info["chunks_created"] = 0
        current_pdf_info["total_pages"] = 0
        return {"message": "All documents cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing data: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
