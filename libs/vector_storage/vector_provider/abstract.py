import hashlib
from abc import ABC, abstractmethod
from typing import List

from libs.embedding.abstract import EmbeddingAbstract
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

    def generate_id(self, doc: Document) -> str:
        return hashlib.md5(doc.title.encode("utf-8") + doc.source.encode("utf-8")).hexdigest()