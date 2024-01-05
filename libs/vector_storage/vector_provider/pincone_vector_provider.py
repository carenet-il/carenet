from abc import ABC
from typing import List

import pinecone
from pinecone import QueryResponse

from libs.embedding.abstract.embedding_abstract import EmbeddingAbstract
from libs.interfaces.document import Document
from libs.vector_storage.vector_provider.abstract.vector_provider_abstract import VectorProviderAbstract


class PineconeVectorProvider(VectorProviderAbstract, ABC):
    def __init__(self, embedding_model: EmbeddingAbstract, index_name: str, api_key: str, environment: str):
        super().__init__(embedding_model)
        self.index_name = index_name
        pinecone.init(api_key=api_key, environment=environment)
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(self.index_name)
        self.index = pinecone.Index(self.index_name)

    def search(self, query: str, filters=None) -> List[Document]:
        query_vector = self.embedding_model.encode(query)  # Encode the query string to a vector
        results: QueryResponse = self.index.query(query_vector, top_k=10, include_metadata=True,
                                                  filter=filters)

        documents: List[Document] = [r.metadata.original_document for r in results.matches]
        return documents

    def insert_many(self, documents: List[Document]):
        items_to_insert = [(doc.id, self.embedding_model.encode(doc.title)) for doc in documents]
        self.index.upsert(items=items_to_insert)
