from google import genai

from app.domain.interfaces.openai_interface import OpenAIServiceInterface
from app.config import GEMINI_API_KEY

class OpenAIClient(OpenAIServiceInterface):
    def __init__(self):
        self._client = genai.Client()

    async def generate_text(self, prompt: str) -> str:
        response = self._client.models.generate_content(    
            model="gemini-2.5-flash", contents=prompt
        )
        return response.text    