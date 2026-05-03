"""
LLM Service
Uses Groq API with llama3-8b-8192 model for generating answers
"""

import os
from typing import List, Dict, Any
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class LLMService:
    """Service for generating answers using Groq API"""
    
    def __init__(self):
        """Initialize the LLM service"""
        # Get API key from environment variable
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            print("Warning: GROQ_API_KEY environment variable not set")
            print("Please set it before starting the server:")
            print("export GROQ_API_KEY='your_api_key_here'")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)
        
        # Model configuration
        self.model = "llama3-8b-8192"  # Free tier model
        self.max_tokens = 1000
        self.temperature = 0.1  # Low temperature for more factual responses
    
    def generate_answer(self, question: str, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Generate an answer based on the question and retrieved context chunks
        
        Args:
            question: User's question
            context_chunks: List of relevant chunks from vector search
            
        Returns:
            Generated answer as a string
        """
        if not self.client:
            return "Error: Groq API key not configured. Please set GROQ_API_KEY environment variable."
        
        try:
            # Create context from retrieved chunks
            context = self._create_context(context_chunks)
            
            # Create the prompt with strict instructions to use only provided context
            prompt = self._create_prompt(question, context)
            
            # Generate response using Groq
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant. Answer questions ONLY using the provided context. Do not use any external knowledge. If the context doesn't contain the answer, say 'I cannot answer this question based on the provided documents.'"
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            answer = chat_completion.choices[0].message.content.strip()
            return answer
            
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def _create_context(self, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Create a formatted context string from retrieved chunks
        
        Args:
            context_chunks: List of chunks with metadata
            
        Returns:
            Formatted context string
        """
        if not context_chunks:
            return "No relevant context found."
        
        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            context_part = f"""
Context {i} (Page {chunk['page_number']}):
{chunk['text']}
"""
            context_parts.append(context_part)
        
        return "\n".join(context_parts)
    
    def _create_prompt(self, question: str, context: str) -> str:
        """
        Create a prompt that instructs the LLM to answer only from context
        
        Args:
            question: User's question
            context: Retrieved context documents
            
        Returns:
            Complete prompt for the LLM
        """
        prompt = f"""
Question: {question}

Context Documents:
{context}

Instructions:
1. Answer the question using ONLY the information provided in the context documents above
2. Do not use any external knowledge or information not present in the context
3. If the context doesn't contain enough information to answer the question, say "I cannot answer this question based on the provided documents"
4. Be concise and direct in your answer
5. Include specific details from the context when relevant

Answer:
"""
        return prompt
    
    def is_configured(self) -> bool:
        """Check if the service is properly configured with API key"""
        return self.client is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model configuration"""
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "configured": self.is_configured()
        }
