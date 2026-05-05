"""
Embedding Service
Uses HuggingFace Inference API for embeddings (no local models, free tier)
"""

import numpy as np
import os
import requests
from typing import List


class EmbeddingService:
    """Service for creating text embeddings using HuggingFace Inference API"""
    
    def __init__(self):
        """Initialize the embedding service with HuggingFace Inference API"""
        self.api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction"
        # Get HF token from environment or use anonymous
        self.hf_token = os.getenv("HUGGINGFACE_API_KEY", "")
        self.model = "sentence-transformers/all-MiniLM-L6-v2"
        self.embedding_dimension = 384
        self.headers = {}
        if self.hf_token:
            self.headers = {"Authorization": f"Bearer {self.hf_token}"}
    
    def create_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """
        Create embeddings for a list of texts using HuggingFace Inference API
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of numpy arrays containing embeddings
        """
        try:
            # Filter out empty texts
            valid_texts = [text for text in texts if text and text.strip()]
            
            if len(valid_texts) == 0:
                return []
            
            # Call HuggingFace Inference API
            payload = {"inputs": valid_texts, "options": {"use_gpu": False}}
            response = requests.post(
                self.api_url,
                headers={**self.headers, "Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"HF API error: {response.text}")
            
            embeddings_data = response.json()
            
            # Convert to numpy arrays and normalize
            embeddings = []
            for emb in embeddings_data:
                arr = np.array(emb, dtype=np.float32)
                # Normalize
                norm = np.linalg.norm(arr)
                if norm > 0:
                    arr = arr / norm
                embeddings.append(arr)
            
            return embeddings
            
        except Exception as e:
            raise Exception(f"Error creating embeddings: {str(e)}")
    
    def create_single_embedding(self, text: str) -> np.ndarray:
        """
        Create embedding for a single text
        
        Args:
            text: Text string to embed
            
        Returns:
            Numpy array containing the embedding
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        embeddings = self.create_embeddings([text])
        # Fix array boolean context issue
        if isinstance(embeddings, np.ndarray):
            return embeddings[0] if embeddings.size > 0 else np.array([])
        else:
            return embeddings[0] if embeddings else np.array([])
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embeddings
        
        Returns:
            Integer representing the embedding dimension
        """
        return self.embedding_dimension
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
            
        Returns:
            Cosine similarity score (0 to 1)
        """
        # Normalize embeddings if not already normalized
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Compute cosine similarity
        similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
        return float(similarity)
