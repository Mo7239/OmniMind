from collections import deque
from typing import List
from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)

class Message:
    def __init__(self, role:str , content:str):
        self.role = role
        self.content = content 

    def to_dict(self) -> dict:
        return {"role":self.role,
                "content":self.content}

class ShortTermMemory:
    def __init__(self):
        self.max_messages = settings.short_term_max_messages
        self.messages : deque = deque(maxlen=self.max_messages)

    def add(self , role:str , content:str) -> None:
        message = Message(role = role , content = content)
        self.messages.append(message)
        logger.debug(f"Added message | role={role}")

    def get_all(self)->List[dict]:
        return [msg.to_dict() for msg in self.messages] 

    def get_as_string(self) -> str:
        return "\n".join(
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in self.get_all()
        )
    
    def clear(self) -> None:
        self.messages.clear()
        logger.info("Short-term memory cleared")

    def __len__(self) -> int:
        return len(self.messages)        