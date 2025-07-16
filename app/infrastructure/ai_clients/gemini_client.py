from google import genai

from app.domain.interfaces.openai_interface import AIServiceInterface
from app.config import GEMINI_API_KEY

class GeminiAIClient(AIServiceInterface):
    def __init__(self):
        self._client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_text(self, prompt: str):
        response_stream = self._client.models.generate_content_stream(    
            model="gemini-2.5-flash", contents=prompt
        )

        for chunk in response_stream:
            yield chunk.text or ""   