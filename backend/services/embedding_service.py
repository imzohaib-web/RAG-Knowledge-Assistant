"""
Embedding Service
Uses HuggingFace Inference API for embeddings (no local models, free tier)
"""

import numpy as np
import os
import requests
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class EmbeddingService:

    """Service for creating text embeddings using HuggingFace Inference API"""

    

    def __init__(self):

        """Initialize the embedding service with HuggingFace Inference API"""

        # Correct HuggingFace Inference API endpoint for feature extraction

        self.model_id = "sentence-transformers/all-MiniLM-L6-v2"

        # Use the standard HuggingFace Inference API endpoint
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_id}"

        # Get HF token from environment or use anonymous

        self.hf_token = os.getenv("HUGGINGFACE_API_KEY", "")

        self.embedding_dimension = 384

        self.headers = {"Content-Type": "application/json"}

        if self.hf_token:

            self.headers["Authorization"] = f"Bearer {self.hf_token}"

            logger.info("HuggingFace API token found")
        else:
            logger.warning("No HuggingFace API token found - using anonymous access (may have rate limits)")

    

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

            

            logger.info(f"Creating embeddings for {len(valid_texts)} texts")
            logger.debug(f"API URL: {self.api_url}")
            
            # Call HuggingFace Inference API with correct format
            payload = {"inputs": valid_texts}
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            logger.info(f"HF API response status: {response.status_code}")

            

            if response.status_code != 200:
                error_msg = f"HF API error: {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)
            
            embeddings_data = response.json()
            logger.debug(f"Received embeddings data type: {type(embeddings_data)}")
            
            # Handle different response formats
            if isinstance(embeddings_data, list) and len(embeddings_data) > 0:
                # Standard case: list of embeddings
                embeddings = []
                for emb in embeddings_data:
                    arr = np.array(emb, dtype=np.float32)
                    # Normalize
                    norm = np.linalg.norm(arr)
                    if norm > 0:
                        arr = arr / norm
                    embeddings.append(arr)
                return embeddings
            elif isinstance(embeddings_data, dict) and 'embeddings' in embeddings_data:
                # Alternative response format
                embeddings = []
                for emb in embeddings_data['embeddings']:
                    arr = np.array(emb, dtype=np.float32)
                    norm = np.linalg.norm(arr)
                    if norm > 0:
                        arr = arr / norm
                    embeddings.append(arr)
                return embeddings
            else:
                raise Exception(f"Unexpected response format: {type(embeddings_data)}")

            

        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
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

