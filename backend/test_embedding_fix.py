#!/usr/bin/env python3
"""
Test script to verify embedding service fixes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.embedding_service import EmbeddingService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_embedding_service():
    """Test the embedding service with sample text"""
    print("Testing Embedding Service...")
    
    try:
        # Initialize the service
        embedding_service = EmbeddingService()
        print(f"✓ Embedding service initialized")
        print(f"  - Model: {embedding_service.model_id}")
        print(f"  - API URL: {embedding_service.api_url}")
        print(f"  - Has API token: {'Yes' if embedding_service.hf_token else 'No'}")
        
        # Test single embedding
        test_text = "This is a test sentence for embedding generation."
        print(f"\nTesting single embedding for: '{test_text}'")
        
        embedding = embedding_service.create_single_embedding(test_text)
        print(f"✓ Single embedding created successfully")
        print(f"  - Shape: {embedding.shape}")
        print(f"  - Type: {type(embedding)}")
        
        # Test multiple embeddings
        test_texts = [
            "First test sentence",
            "Second test sentence", 
            "Third test sentence"
        ]
        print(f"\nTesting multiple embeddings for {len(test_texts)} texts...")
        
        embeddings = embedding_service.create_embeddings(test_texts)
        print(f"✓ Multiple embeddings created successfully")
        print(f"  - Number of embeddings: {len(embeddings)}")
        print(f"  - Shape of first embedding: {embeddings[0].shape if embeddings else 'N/A'}")
        
        # Test similarity computation
        if len(embeddings) >= 2:
            similarity = embedding_service.compute_similarity(embeddings[0], embeddings[1])
            print(f"✓ Similarity computation works")
            print(f"  - Similarity between first two embeddings: {similarity:.4f}")
        
        print(f"\n🎉 All embedding service tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Embedding service test failed: {str(e)}")
        logger.error(f"Embedding test error: {str(e)}")
        return False

def test_api_connectivity():
    """Test basic API connectivity"""
    print("\nTesting API Connectivity...")
    
    try:
        import requests
        
        # Test HuggingFace API connectivity
        hf_url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
        response = requests.get(hf_url, timeout=10)
        
        if response.status_code in [200, 401, 429]:  # These are expected responses
            print(f"✓ HuggingFace API is reachable")
            print(f"  - Status code: {response.status_code}")
            if response.status_code == 401:
                print("  - Note: API key required for full functionality")
            elif response.status_code == 429:
                print("  - Note: Rate limited (anonymous access)")
        else:
            print(f"⚠️ Unexpected API response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ API connectivity test failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("RAG System - Embedding Service Test")
    print("=" * 50)
    
    # Test API connectivity first
    api_ok = test_api_connectivity()
    
    # Test embedding service
    embedding_ok = test_embedding_service()
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"API Connectivity: {'✓ PASS' if api_ok else '❌ FAIL'}")
    print(f"Embedding Service: {'✓ PASS' if embedding_ok else '❌ FAIL'}")
    
    if api_ok and embedding_ok:
        print("\n🎉 All tests passed! The embedding service is working correctly.")
        sys.exit(0)
    else:
        print("\n⚠️ Some tests failed. Check the logs above for details.")
        sys.exit(1)
