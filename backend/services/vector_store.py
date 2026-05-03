"""
Vector Store Service
Uses FAISS for local vector storage and similarity search
"""

import os
import pickle
import numpy as np
from typing import List, Dict, Any, Optional
import faiss


class VectorStore:
    """Service for storing and searching text embeddings using FAISS"""
    
    def __init__(self, index_path: str = "vector_store/faiss_index"):
        """Initialize the vector store"""
        self.index_path = index_path
        self.metadata_path = f"{index_path}_metadata.pkl"
        self.index = None
        self.metadata = []  # Store chunk metadata (text, page numbers, etc.)
        self.embedding_dimension = 384  # For all-MiniLM-L6-v2
        
        # Load existing index if available
        self._load_index()
    
    def store_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[np.ndarray]):
        """
        Store chunks and their embeddings in FAISS index
        
        Args:
            chunks: List of chunk dictionaries with metadata
            embeddings: List of numpy arrays containing embeddings
        """
        try:
            if not chunks:
                raise ValueError("No chunks provided")

            # Convert embeddings to numpy array safely (works for lists and ndarrays)
            if isinstance(embeddings, np.ndarray):
                embedding_array = embeddings
            else:
                embedding_array = np.array(embeddings, dtype="float32")

            if embedding_array.size == 0:
                raise ValueError("No embeddings provided")

            # Ensure embeddings are 2D: (n_vectors, embedding_dimension)
            if embedding_array.ndim == 1:
                embedding_array = embedding_array.reshape(1, -1)

            if embedding_array.ndim != 2:
                raise ValueError("Embeddings must be a 2D array")

            if embedding_array.shape[0] != len(chunks):
                raise ValueError(
                    f"Chunks/embeddings count mismatch: {len(chunks)} chunks, "
                    f"{embedding_array.shape[0]} embeddings"
                )

            if embedding_array.shape[1] != self.embedding_dimension:
                raise ValueError(
                    f"Embedding dimension mismatch: expected {self.embedding_dimension}, "
                    f"got {embedding_array.shape[1]}"
                )
            
            # Create FAISS index if it doesn't exist
            if self.index is None:
                self.index = faiss.IndexFlatIP(self.embedding_dimension)  # Inner Product for cosine similarity
            
            # Add embeddings to index
            self.index.add(embedding_array.astype("float32"))
            
            # Store metadata
            for chunk in chunks:
                self.metadata.append({
                    "text": chunk["text"],
                    "page_number": chunk["page_number"],
                    "chunk_id": chunk["chunk_id"]
                })
            
            # Save to disk
            self._save_index()
            
        except Exception as e:
            raise Exception(f"Error storing chunks: {str(e)}")
    
    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for most similar chunks
        
        Args:
            query_embedding: Embedding of the query
            top_k: Number of top results to return
            
        Returns:
            List of similar chunks with metadata
        """
        try:
            if self.index is None or self.index.ntotal == 0:
                return []
            
            # Reshape query embedding for FAISS
            query_embedding = query_embedding.reshape(1, -1).astype('float32')
            
            # Search for similar embeddings
            similarities, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))
            
            # Get results
            results = []
            for i, (similarity, idx) in enumerate(zip(similarities[0], indices[0])):
                if idx >= 0 and idx < len(self.metadata):  # Valid index
                    chunk_data = self.metadata[idx].copy()
                    chunk_data["similarity_score"] = float(similarity)
                    results.append(chunk_data)
            
            return results
            
        except Exception as e:
            raise Exception(f"Error searching vector store: {str(e)}")
    
    def has_data(self) -> bool:
        """Check if the vector store contains any data"""
        return self.index is not None and self.index.ntotal > 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        if self.index is None:
            return {"total_chunks": 0, "index_size_mb": 0}
        
        # Calculate approximate index size in memory
        index_size = self.index.ntotal * self.embedding_dimension * 4  # 4 bytes per float32
        index_size_mb = index_size / (1024 * 1024)
        
        return {
            "total_chunks": self.index.ntotal,
            "index_size_mb": round(index_size_mb, 2),
            "embedding_dimension": self.embedding_dimension
        }
    
    def clear_store(self):
        """Clear all stored data"""
        self.index = None
        self.metadata = []
        self._delete_index_files()
    
    def _save_index(self):
        """Save FAISS index and metadata to disk"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
            
            # Save FAISS index
            if self.index is not None:
                faiss.write_index(self.index, self.index_path)
            
            # Save metadata
            with open(self.metadata_path, 'wb') as f:
                pickle.dump(self.metadata, f)
                
        except Exception as e:
            raise Exception(f"Error saving index: {str(e)}")
    
    def _load_index(self):
        """Load FAISS index and metadata from disk"""
        try:
            # Load FAISS index
            if os.path.exists(self.index_path):
                self.index = faiss.read_index(self.index_path)
            
            # Load metadata
            if os.path.exists(self.metadata_path):
                with open(self.metadata_path, 'rb') as f:
                    self.metadata = pickle.load(f)
                    
        except Exception as e:
            # If loading fails, start fresh
            print(f"Warning: Could not load existing index: {str(e)}")
            self.index = None
            self.metadata = []
    
    def _delete_index_files(self):
        """Delete index and metadata files"""
        try:
            if os.path.exists(self.index_path):
                os.remove(self.index_path)
            if os.path.exists(self.metadata_path):
                os.remove(self.metadata_path)
        except Exception as e:
            print(f"Warning: Could not delete index files: {str(e)}")
