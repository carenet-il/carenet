from abc import ABC, abstractmethod
from typing import List


class EmbeddingAbstract(ABC):
    @abstractmethod
    def request_rerank(self, query: str, texts: tuple[str]) -> List[str]:
        pass
    @abstractmethod
    def encode(self, text: str) -> List[float]:
        pass

    @abstractmethod
    def encode_bulk(self, texts: List[str]) -> List[List[float]]:
        pass