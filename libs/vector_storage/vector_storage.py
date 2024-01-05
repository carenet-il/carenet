from typing import List

from libs.interfaces.document import Document
from libs.vector_storage.vector_provider.abstract.vector_provider_abstract import VectorProviderAbstract


class VectorStorage:
    def __init__(self, storage_provider: VectorProviderAbstract):
        self.storage_provider = storage_provider

    def insert_documents(self, norm_documents: List[Document]):
        return self.storage_provider.insert_many(norm_documents)

    def search(self, query, filters=None):
        if filters is None:
            filters = {}

        return self.storage_provider.search(query, filters)
