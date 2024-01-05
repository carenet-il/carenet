from abc import ABC
from typing import List

from libs.embedding.abstract.embedding_abstract import EmbeddingAbstract


class MiniLMv6Embedding(EmbeddingAbstract, ABC):

    def __init__(self):
        pass

    def encode(self, text: str) -> List[float]:
        return [1, 2, 3]
