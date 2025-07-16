from abc import ABC, abstractmethod

class AIServiceInterface(ABC):
    @abstractmethod
    async def generate_text(self, prompt: str) -> str:
        pass