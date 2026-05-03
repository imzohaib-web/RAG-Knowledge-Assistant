# RAG Knowledge Assistant

A full-stack Retrieval-Augmented Generation (RAG) web application that lets users upload PDF documents and ask questions about their content. The backend extracts text, creates embeddings, stores them in a local FAISS vector database, and uses the Groq API to generate answers with source references.

## Features

- Upload and process PDF documents
- Extract PDF text with `pdfplumber`
- Split text into searchable chunks
- Generate embeddings using Hugging Face `sentence-transformers`
- Store vectors locally with FAISS
- Ask document-based questions through a chat interface
- Show source pages and relevant chunks
- Save chat history and feedback
- React frontend with a clean responsive UI

## Tech Stack

**Frontend**

- React
- Vite
- Tailwind CSS

**Backend**

- Python
- FastAPI
- LangChain text splitters
- Sentence Transformers
- FAISS
- Groq API

## Project Structure

```text
Rag system/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── services/
│   ├── README.md
│   └── .gitignore
├── rag-ui/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
├── start_system.bat
└── README.md
```

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- npm
- Git
- Groq API key

## Environment Variables

Create a `.env` file inside the `backend` folder:

```env
GROQ_API_KEY=your_groq_api_key_here
```

The `.env` file is intentionally ignored by Git and should not be uploaded to GitHub.

## Backend Setup

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend server:

```bash
python main.py
```

The backend will run at:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

## Frontend Setup

Open a new terminal:

```bash
cd rag-ui
npm install
npm run dev
```

The frontend will run at:

```text
http://localhost:5173
```

## Quick Start On Windows

You can also use the included batch file:

```powershell
.\start_system.bat
```

This starts both the backend and frontend in separate terminal windows.

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Health check |
| `POST` | `/upload` | Upload and process a PDF |
| `POST` | `/chat` | Ask questions about uploaded PDF content |
| `GET` | `/settings` | Get current RAG settings |
| `POST` | `/settings` | Update chunking, model, and retrieval settings |
| `GET` | `/history/get` | Get saved chat history |
| `POST` | `/feedback` | Save user feedback |
| `GET` | `/pdf-info` | Get current uploaded PDF info |
| `DELETE` | `/clear` | Clear stored document vectors |

## Usage

1. Start the backend server.
2. Start the frontend development server.
3. Open the frontend in your browser.
4. Upload a PDF document.
5. Ask questions about the uploaded document.
6. Review the answer and source pages.

## Important Notes

- Only PDF upload is supported by the backend.
- Uploaded files are processed locally.
- Vector data is stored locally in the backend.
- Groq API is used for answer generation.
- Do not commit `.env`, API keys, virtual environments, uploads, or vector store files.

## GitHub Upload

Before pushing, check that sensitive files are not tracked:

```bash
git status
git ls-files *env*
```

Then push your changes:

```bash
git add .
git commit -m "Add project README"
git push
```

## License

This project is for educational and learning purposes.
