# Environment Configuration Setup

## Overview
The RAG Knowledge Assistant frontend uses environment variables to configure the API endpoint. This ensures the app works correctly in both development and production environments.

## Environment Variables

### VITE_API_URL
- **Purpose**: Defines the backend API base URL
- **Development**: `http://localhost:8000` (when running backend locally)
- **Production**: `https://rag-knowledge-assistant-3tgm.onrender.com` (deployed backend)

## Setup Instructions

### 1. Development Setup
Copy the example environment file:
```bash
cp .env.example .env
```

For local development with a running backend:
```env
VITE_API_URL=http://localhost:8000
```

### 2. Production Setup
The production environment variable is already set in `.env`:
```env
VITE_API_URL=https://rag-knowledge-assistant-3tgm.onrender.com
```

### 3. Deployment (Vercel)
Environment variables are automatically read from `.env` during build. Ensure the production URL is set before deploying.

## Error Handling
The frontend now provides clear error messages when:
- Backend server is not running or unreachable
- CORS issues occur
- Network connectivity problems exist

## API Configuration Logic
The API service uses the following priority:
1. `VITE_API_URL` environment variable (if set)
2. Falls back to `http://localhost:8000` for development

This ensures the app works seamlessly between local development and production deployment.
