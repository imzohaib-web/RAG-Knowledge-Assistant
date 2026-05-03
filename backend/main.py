"""
RAG Knowledge Assistant Backend
FastAPI application for PDF processing, embeddings, and chat functionality
"""

import os
import uuid
from typing import List, Dict, Any
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

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_created: int

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("vector_store", exist_ok=True)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "RAG Knowledge Assistant API is running"}

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
        
        # Chunk the text
        chunks = text_chunker.chunk_text(extracted_text)
        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Failed to create text chunks from the uploaded PDF."
            )
        
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
        
        return UploadResponse(
            message="PDF processed successfully",
            filename=file.filename,
            chunks_created=len(chunks)
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
        
        # Create embedding for the question
        question_embedding = embedding_service.create_embeddings([request.question])[0]
        
        # Search for relevant chunks
        relevant_chunks = vector_store.search(question_embedding, top_k=3)
        
        # Generate answer using LLM
        answer = llm_service.generate_answer(request.question, relevant_chunks)
        
        # Extract source page numbers
        sources = [f"Page {chunk['page_number']}" for chunk in relevant_chunks]
        
        return ChatResponse(
            answer=answer,
            sources=list(set(sources))  # Remove duplicates
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@app.delete("/clear")
async def clear_data():
    """Clear all stored documents and embeddings"""
    try:
        vector_store.clear_store()
        return {"message": "All documents cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing data: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
