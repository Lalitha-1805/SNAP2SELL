"""
Gemini API Client for RAG
Uses Google Gemini Flash with strict context-only system prompt
"""

import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False
    logger.warning('google.generativeai not installed; Gemini client unavailable')


class GeminiClient:
    """
    Wrapper for Google Gemini Flash API.
    Enforces strict RAG rules: answer ONLY from context.
    """
    
    SYSTEM_PROMPT = """You are AgriSmart, a professional agriculture assistant for Indian farmers.

CRITICAL RULES:
1. Answer ONLY using the provided Context.
2. Do NOT use outside knowledge or make up information.
3. If the answer is not in the Context, respond exactly:
   "I don't have enough information to answer this question."
4. Be concise and practical.
5. Use bullet points for clarity.
6. Focus on the asked crop only.
7. Do NOT mix information from different crops.
8. Avoid repetition and long paragraphs.
9. If context is missing or unclear, say so clearly.

Remember: Your credibility depends on staying within the provided context."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('GOOGLE_API_KEY')
        self.client_available = False
        
        if not self.api_key:
            logger.warning('GOOGLE_API_KEY not set; Gemini API will not be available')
            return
        
        if not HAS_GEMINI:
            logger.warning('google.generativeai package not installed')
            return
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.client_available = True
            logger.info('[OK] Gemini Flash client initialized')
        except Exception as e:
            logger.error(f'[ERROR] Failed to initialize Gemini: {e}')
            self.client_available = False
    
    def generate_answer(self, question: str, context: str) -> str:
        """
        Generate answer using Gemini Flash with strict RAG constraints.
        
        Args:
            question: User's question
            context: Retrieved documents as context
        
        Returns:
            Answer string (context-only or fallback message)
        """
        if not self.client_available:
            return "Gemini service is not available. Please check API configuration."
        
        if not context or context.strip() == '':
            return "I don't have enough information to answer this question."
        
        # Build prompt: system + context + question
        prompt = f"""Context:
{context}

Question:
{question}

Answer:"""
        
        try:
            response = self.model.generate_content(
                prompt,
                system_instruction=self.SYSTEM_PROMPT,
                generation_config={
                    'temperature': 0.2,  # Low temperature for consistency
                    'top_p': 0.9,
                    'max_output_tokens': 500
                }
            )
            
            answer = response.text.strip()
            if not answer:
                return "I don't have enough information to answer this question."
            return answer
        
        except Exception as e:
            logger.error(f'[ERROR] Gemini API call failed: {e}')
            return "Service error. Please try again."
    
    def is_available(self) -> bool:
        """Check if Gemini client is ready"""
        return self.client_available
