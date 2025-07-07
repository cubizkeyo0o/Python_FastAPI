from infrastructure.openai.openai_client import OpenAIClient

class OpenAIService:
    def __init__(self, client: OpenAIClient):
        self._client = client

    async def generate_response(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise ValueError("Prompt must not be empty.")
        
        response = await self._client.generate_text(prompt)
        return response
    