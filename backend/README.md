# RAG Knowledge Assistant Backend

FastAPI backend for the RAG (Retrieval-Augmented Generation) AI Knowledge Assistant.

## Features

- **PDF Processing**: Extract text from PDF files using pdfplumber
- **Text Chunking**: Split documents into 500-word chunks with 50-word overlap
- **Embeddings**: Create vector embeddings using HuggingFace sentence-transformers (all-MiniLM-L6-v2)
- **Vector Storage**: Local FAISS vector database for similarity search
- **LLM Integration**: Groq API with llama3-8b-8192 model for answer generation
- **CORS Support**: Configured for React frontend integration

## Tech Stack

- **Backend**: FastAPI (Python)
- **PDF Processing**: pdfplumber
- **Text Chunking**: LangChain RecursiveCharacterTextSplitter
- **Embeddings**: HuggingFace sentence-transformers (all-MiniLM-L6-v2)
- **Vector Database**: FAISS (local)
- **LLM**: Groq API (llama3-8b-8192)

## Setup Instructions

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up Groq API Key

1. Sign up for a free Groq account at [https://groq.com](https://groq.com)
2. Get your API key from the dashboard
3. Set the environment variable:

```bash
# Windows
set GROQ_API_KEY=your_api_key_here

# Mac/Linux
export GROQ_API_KEY=your_api_key_here
```

### 3. Start the Backend Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/` - Health check endpoint

### PDF Upload
- **POST** `/upload` - Upload and process PDF files
  - Accepts: PDF file
  - Returns: Upload confirmation with chunk count

### Chat/Query
- **POST** `/chat` - Ask questions about uploaded documents
  - Body: `{"question": "your question here"}`
  - Returns: `{"answer": "response", "sources": ["Page 1", "Page 3"]}`

### Clear Data
- **DELETE** `/clear` - Clear all stored documents and embeddings

## Usage Examples

### Upload a PDF

```bash
curl -X POST "http://localhost:8000/upload" -F "file=@document.pdf"
```

### Ask a Question

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

### Clear All Data

```bash
curl -X DELETE "http://localhost:8000/clear"
```

## File Structure

```
backend/
├── main.py                 # Main FastAPI application
├── requirements.txt        # Python dependencies
├── services/              # Service modules
│   ├── __init__.py
│   ├── pdf_processor.py   # PDF text extraction
│   ├── text_chunker.py    # Text chunking with LangChain
│   ├── embedding_service.py # HuggingFace embeddings
│   ├── vector_store.py    # FAISS vector database
│   └── llm_service.py     # Groq LLM integration
├── uploads/               # Temporary file storage
└── vector_store/          # FAISS index storage
```

## Configuration

- **Chunk Size**: 500 words (approximately 2000 characters)
- **Chunk Overlap**: 50 words (approximately 200 characters)
- **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
- **LLM Model**: llama3-8b-8192 via Groq API
- **Search Results**: Top 3 most relevant chunks

## Important Notes

- Only PDF files are supported
- All processing happens locally (except LLM calls)
- FAISS index is saved to disk for persistence
- No external vector database needed
- Groq API free tier is sufficient for basic usage

## Troubleshooting

### Common Issues

1. **"GROQ_API_KEY not set"**
   - Make sure to set the environment variable before starting the server

2. **"No documents uploaded yet"**
   - Upload a PDF file before asking questions

3. **"Only PDF files are allowed"**
   - Ensure you're uploading PDF files with .pdf extension

4. **CORS errors in frontend**
   - Make sure backend is running on port 8000
   - Check that frontend is on localhost:3000 or localhost:5173

## Development

To run in development mode with auto-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## License

This project uses only FREE and open-source components.
