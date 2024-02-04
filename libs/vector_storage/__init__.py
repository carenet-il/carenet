import os
from typing import List, Optional

from libs.embedding.quora_distilbert_multilingual_embedding import (
    QuoraDistilBertMultilingualEmbedding,
)
from libs.interfaces.document import Document, DocumentSearchFilters
from libs.vector_storage.vector_provider.abstract import VectorProviderAbstract
from libs.vector_storage.vector_provider.pincone_vector_provider import (
    PineconeVectorProvider,
)
from libs.utils.cache import lru_cache_with_ttl


class VectorStorage:
    def __init__(self, storage_provider: VectorProviderAbstract):
        self.storage_provider = storage_provider

    def insert_documents(self, norm_documents: List[Document]):
        return self.storage_provider.insert_many(norm_documents)

    def delete_all(self):
        return self.storage_provider.delete_all()

    def search(self, query, filters: Optional[DocumentSearchFilters] = None):
        if filters is None:
            filters = {}

        return self.storage_provider.search(query, filters)

    # I am using no maxsize for the cache, since there is only one argument, and it is the same for all calls.
    @lru_cache_with_ttl(maxsize=None, ttl=120)
    def fetch_search_filters(self):
        return self.storage_provider.fetch_search_filters()
    

if __name__ == "__main__":
    embedding_model = QuoraDistilBertMultilingualEmbedding(load_locally_model=True)

    storage_provider = PineconeVectorProvider(
        embedding_model=embedding_model,
        api_key=os.getenv("PINECONE_API_KEY"),
        environment=os.getenv("PINECONE_ENVIRONMENT"),
        index_name=os.getenv("PINECONE_INDEX_NAME"),
    )

    vector_storage = VectorStorage(storage_provider=storage_provider)

    vector_storage.delete_all()
    print('After delete all data from db')
    # query = "משפחות השבויים והנעדרים"
    # # filters = {"state": "מחוז הדרום"}
    # filters = {}
    # results = vector_storage.search(query=query, filters=filters)
    # pprint(results)
