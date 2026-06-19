from abc import ABC, abstractmethod
from typing import Generator


class BaseLLM(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

    @abstractmethod
    def stream(self, prompt: str) -> Generator[str, None, None]:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass