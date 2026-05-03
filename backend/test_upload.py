#!/usr/bin/env python3
"""
Test script to debug PDF upload issues
"""

import requests
import os

def test_backend():
    """Test backend endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing Backend...")
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/")
        print(f"✓ Health check: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False
    
    # Test upload with a simple file
    try:
        # Create a test PDF file (simple text file with .pdf extension for testing)
        test_file_path = "test_document.pdf"
        with open(test_file_path, "w") as f:
            f.write("This is a test document for debugging upload issues.")
        
        with open(test_file_path, "rb") as f:
            files = {"file": (test_file_path, f, "application/pdf")}
            response = requests.post(f"{base_url}/upload", files=files)
        
        print(f"✓ Upload test: {response.status_code}")
        if response.status_code != 200:
            print(f"  Error: {response.text}")
        else:
            print(f"  Response: {response.json()}")
        
        # Clean up
        os.remove(test_file_path)
        
    except Exception as e:
        print(f"✗ Upload test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_backend()
