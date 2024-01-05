from abc import ABC, abstractmethod
from typing import List


class EmbeddingAbstract(ABC):

    @abstractmethod
    def encode(self, text: str) -> List[float]:
        pass
