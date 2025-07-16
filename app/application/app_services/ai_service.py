from fastapi import Depends

from app.infrastructure.ai_clients.gemini_client import GeminiAIClient
from app.infrastructure.ai_clients.openai_client import OpenAIClient
from app.utils.exceptions.common_exceptions import RequiredException

class AIService:
    _gemini_client: GeminiAIClient
    _openai_client: OpenAIClient

    def __init__(self,
                 gemini_client: GeminiAIClient = Depends(GeminiAIClient),
                 openai_client: OpenAIClient = Depends(OpenAIClient)):
        self._gemini_client = gemini_client
        self._openai_client = openai_client

    def prompt_gemini(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise RequiredException("Prompt must not be empty.")
        
        response = self._gemini_client.generate_text(prompt)
        return response
    