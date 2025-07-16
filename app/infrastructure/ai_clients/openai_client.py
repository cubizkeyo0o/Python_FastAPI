from openai import AsyncOpenAI

from app.domain.interfaces.openai_interface import AIServiceInterface
from app.config import OPENAI_API_KEY

class OpenAIClient(AIServiceInterface):
    def __init__(self):
        self._client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def generate_text(self, prompt: str, max_tokens: int = 10, limit_output: int = 5):
        response_stream = await self._client.completions.with_streaming_response.create(    
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=max_tokens,
            n=limit_output
        )

        for chunk in response_stream:
            yield chunk.text or ""   