from openai import AsyncOpenAI

from domain.interfaces.openai_interface import OpenAIServiceInterface
from config import OPENAI_API_KEY

class OpenAIClient(OpenAIServiceInterface):
    def __init__(self):
        self._client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def generate_text(self, prompt: str, MaxToken = 50, outputs = 1) -> str:
        response = await self._client.completions.create(    
            model="gpt-4",
            max_tokens= MaxToken,
            prompt=prompt,
            n=outputs
        )
        return response.choices[0].text