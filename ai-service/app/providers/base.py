from abc import ABC, abstractmethod


class LLMProvider(ABC):
    provider_name = "base"

    @abstractmethod
    def generate_json(self, prompt: str) -> str:
        raise NotImplementedError
