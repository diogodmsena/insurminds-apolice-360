from abc import ABC, abstractmethod
from typing import Any, Dict
import logging

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"agent.{name}")

    @abstractmethod
    def run(self, input_data: Any) -> Any:
        pass
