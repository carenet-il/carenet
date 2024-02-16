from abc import ABC, abstractmethod
from typing import List


class EmbeddingAbstract(ABC):

    @abstractmethod
    def encode(self, text: str) -> List[float]:
        pass

    @abstractmethod
    def encode_bulk(self, texts: List[str]) -> List[List[float]]:
        pass