from abc import ABC, abstractmethod

class OpenAIServiceInterface(ABC):
    @abstractmethod
    async def generate_text(self, prompt: str) -> str:
        pass