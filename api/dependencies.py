from functools import lru_cache
from agents.orchestrator import Orchestrator

@lru_cache(maxsize=1)
def get_orchestrator() -> Orchestrator:
    return Orchestrator()