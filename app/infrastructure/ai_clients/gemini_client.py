from google import genai

from app.domain.interfaces.openai_interface import AIServiceInterface
from app.config import GEMINI_API_KEY
from app.utils.enums.key_cache import KeyCache

class GeminiAIClient(AIServiceInterface):
    def __init__(self):
        self._client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_text(self, context: dict):
        return self._client.models.generate_content_stream(    
            model="gemini-2.5-flash",
            contents=context[KeyCache.RECENT_MESSAGES]
        )