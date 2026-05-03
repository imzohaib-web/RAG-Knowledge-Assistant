"""
Embedding Service
Uses HuggingFace sentence-transformers to create text embeddings locally
"""

import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Service for creating text embeddings using HuggingFace models"""
    
    def __init__(self):
        """Initialize the embedding service with all-MiniLM-L6-v2 model"""
        # This model runs locally, no API key needed
        # Model size: ~90MB, good for local use
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dimension = 384  # Dimension for all-MiniLM-L6-v2
    
    def create_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """
        Create embeddings for a list of texts
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of numpy arrays containing embeddings
        """
        try:
            # Filter out empty texts
            valid_texts = [text for text in texts if text and text.strip()]
            
            if not valid_texts:
                return []
            
            # Create embeddings using the HuggingFace model
            embeddings = self.model.encode(
                valid_texts,
                batch_size=32,  # Process in batches for efficiency
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=True  # Normalize for better similarity search
            )
            
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
