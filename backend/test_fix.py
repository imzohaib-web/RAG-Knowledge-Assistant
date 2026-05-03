#!/usr/bin/env python3
"""
Test script to verify the array ambiguity fix
"""

import numpy as np
from services.embedding_service import EmbeddingService
from services.vector_store import VectorStore

def test_embedding_service():
    """Test the embedding service fix"""
    print("Testing EmbeddingService...")
    
    try:
        embedding_service = EmbeddingService()
        
        # Test create_embeddings
        texts = ["This is a test document", "Another test document"]
        embeddings = embedding_service.create_embeddings(texts)
        print(f"✓ create_embeddings works: {type(embeddings)}")
        
        # Test create_single_embedding
        single_embedding = embedding_service.create_single_embedding("Test text")
        print(f"✓ create_single_embedding works: {type(single_embedding)}")
        
        return True
    except Exception as e:
        print(f"✗ EmbeddingService test failed: {e}")
        return False

def test_vector_store():
    """Test the vector store fix"""
    print("Testing VectorStore...")
    
    try:
        vector_store = VectorStore()
        
        # Create test data
        chunks = [
            {"text": "Test chunk 1", "page_number": 1, "chunk_id": 1},
            {"text": "Test chunk 2", "page_number": 1, "chunk_id": 2}
        ]
        
        # Create test embeddings (numpy arrays)
        embeddings = np.array([
            np.random.rand(384),  # all-MiniLM-L6-v2 dimension
            np.random.rand(384)
        ])
        
        # Test store_chunks
        vector_store.store_chunks(chunks, embeddings)
        print("✓ store_chunks works with numpy arrays")
        
        # Test search
        query_embedding = np.random.rand(384)
        results = vector_store.search(query_embedding)
        print(f"✓ search works: found {len(results)} results")
        
        return True
    except Exception as e:
        print(f"✗ VectorStore test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing array ambiguity fixes...\n")
    
    embedding_ok = test_embedding_service()
    print()
    vector_ok = test_vector_store()
    print()
    
    if embedding_ok and vector_ok:
        print("✓ All tests passed! The array ambiguity issue should be fixed.")
    else:
        print("✗ Some tests failed. There may still be issues.")

if __name__ == "__main__":
    main()
