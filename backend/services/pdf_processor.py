"""
PDF Processing Service
Uses pdfplumber to extract text from PDF files with page numbers
"""

import pdfplumber
import re
from typing import Dict, List, Any


class PDFProcessor:
    """Service for processing PDF files and extracting text"""
    
    def __init__(self):
        """Initialize the PDF processor"""
        pass
    
    def extract_text(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extract text from PDF file with page numbers
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of dictionaries containing text and page numbers
            [{"text": "extracted text", "page_number": 1}, ...]
        """
        extracted_pages = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text from the page
                    text = page.extract_text()
                    
                    if text:
                        # Clean the text
                        cleaned_text = self._clean_text(text)
                        
                        if cleaned_text.strip():
                            extracted_pages.append({
                                "text": cleaned_text,
                                "page_number": page_num
                            })
        
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
        
        return extracted_pages
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text by removing extra whitespace and fixing common issues
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Fix common PDF extraction issues
        # Remove bullet points that might be malformed
        text = re.sub(r'[•·]', '•', text)
        
        # Fix hyphenated words at line breaks
        text = re.sub(r'(\w+)-\s*(\w+)', r'\1\2', text)
        
        # Remove page numbers and headers/footers (common patterns)
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip lines that are likely page numbers or headers
            if (line.isdigit() or 
                re.match(r'^page \d+$', line.lower()) or
                len(line) < 3):
                continue
            cleaned_lines.append(line)
        
        return ' '.join(cleaned_lines)
