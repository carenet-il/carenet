from abc import ABC
from typing import List

from libs.embedding.abstract.embedding_abstract import EmbeddingAbstract
from libs.interfaces.document import Document
from libs.vector_storage.vector_provider.abstract.vector_provider_abstract import VectorProviderAbstract


class PineconeVectorProvider(VectorProviderAbstract, ABC):
    def __init__(self, embedding_model: EmbeddingAbstract):
        super().__init__(embedding_model)

    def search(self, query: str, filters=None):
        pass

    def insert_many(self, documents: List[Document]):
        pass
