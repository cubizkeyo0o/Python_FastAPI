from fastapi import Depends

from app.infrastructure.openai.openai_client import OpenAIClient
from app.utils.exceptions.common_exceptions import RequiredException

class OpenAIService:
    _client: OpenAIClient

    def __init__(self, client: OpenAIClient = Depends(OpenAIClient)):
        self._client = client

    async def generate_response(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise RequiredException("Prompt must not be empty.")
        
        response = await self._client.generate_text(prompt)
        return response
    