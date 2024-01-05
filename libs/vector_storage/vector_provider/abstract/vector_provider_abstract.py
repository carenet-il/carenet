from abc import ABC, abstractmethod
from typing import List

from libs.embedding.abstract.embedding_abstract import EmbeddingAbstract
from libs.interfaces.document import Document


class VectorProviderAbstract(ABC):

    def __init__(self, embedding_model: EmbeddingAbstract):
        self.embedding_model = embedding_model

    @abstractmethod
    def insert_many(self, documents: List[Document]):
        pass

    @abstractmethod
    def search(self, query: str, filters=None) -> List[Document]:
        pass
