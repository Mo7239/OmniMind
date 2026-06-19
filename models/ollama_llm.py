import requests
import json
from typing import Generator
from models.base_llm import BaseLLM
from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)


class OllamaLLM(BaseLLM):

    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model

    def generate(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False}
            )
            response.raise_for_status()
            result = response.json()["response"]
            logger.info(f"Generated response | model={self.model}")
            return result

        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise

    def stream(self, prompt: str) -> Generator[str, None, None]:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": True},
                stream=True
            )
            response.raise_for_status()

            buffer = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    token = chunk.get("response", "")
                    buffer += token

                    while " " in buffer:
                        word, buffer = buffer.split(" ", 1)
                        yield word + " "

                    if chunk.get("done") and buffer:
                        yield buffer
                        break

        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            raise

    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False