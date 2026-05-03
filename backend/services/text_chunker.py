"""
Text Chunking Service
Uses LangChain RecursiveCharacterTextSplitter to chunk text with overlap
"""

from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:
    """Service for chunking text into smaller pieces with overlap"""
    
    def __init__(self):
        """Initialize the text chunker with specified parameters"""
        # Chunk size: 500 words (approximately 2000 characters)
        # Chunk overlap: 50 words (approximately 200 characters)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,  # Approximate characters for 500 words
            chunk_overlap=200,  # Approximate characters for 50 words
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def chunk_text(self, extracted_pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Chunk extracted text from PDF pages
        
        Args:
            extracted_pages: List of dictionaries with text and page numbers
            
        Returns:
            List of chunked text with metadata including page numbers
        """
        chunks = []
        
        # Combine all pages into one text for better chunking
        full_text = ""
        page_mapping = []  # Track which page each character comes from
        
        for page in extracted_pages:
            start_pos = len(full_text)
            full_text += page["text"] + "\n\n"  # Add spacing between pages
            end_pos = len(full_text)
            page_mapping.extend([page["page_number"]] * (end_pos - start_pos))
        
        # Split the text into chunks
        text_chunks = self.splitter.split_text(full_text)
        
        # Create chunks with page number metadata
        for i, chunk_text in enumerate(text_chunks):
            if chunk_text.strip():
                # Find the original page number for this chunk
                # Use the first character's page as the chunk's page
                chunk_start_in_full = full_text.find(chunk_text)
                
                if chunk_start_in_full >= 0 and chunk_start_in_full < len(page_mapping):
                    page_number = page_mapping[chunk_start_in_full]
                else:
                    # Fallback: use the most recent page
                    page_number = extracted_pages[-1]["page_number"] if extracted_pages else 1
                
                chunks.append({
                    "text": chunk_text.strip(),
                    "page_number": page_number,
                    "chunk_id": i + 1
                })
        
        return chunks
    
    def get_chunk_metadata(self, chunk: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get metadata for a chunk including word count and character count
        
        Args:
            chunk: Chunk dictionary
            
        Returns:
            Dictionary with chunk metadata
        """
        text = chunk["text"]
        words = len(text.split())
        characters = len(text)
        
        return {
            "chunk_id": chunk["chunk_id"],
            "page_number": chunk["page_number"],
            "word_count": words,
            "character_count": characters,
            "text_preview": text[:100] + "..." if len(text) > 100 else text
        }
