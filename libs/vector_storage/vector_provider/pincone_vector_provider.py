from abc import ABC
from typing import List, Optional

import pinecone
from pinecone import QueryResponse

from libs.embedding.abstract import EmbeddingAbstract
from libs.interfaces.document import Document, EmbeddingDocument, DocumentSearchFilters
from libs.vector_storage.vector_provider.abstract import VectorProviderAbstract


class PineconeVectorProvider(VectorProviderAbstract, ABC):
    def __init__(
        self,
        embedding_model: EmbeddingAbstract,
        index_name: str,
        api_key: str,
        environment: str,
    ):
        super().__init__(embedding_model)
        self.index_name = index_name
        pinecone.init(api_key=api_key, environment=environment)
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(self.index_name)
        self.index = pinecone.Index(self.index_name)

    def search(
        self, query: str, filters: Optional[DocumentSearchFilters] = None
    ) -> List[Document]:
        if not filters:
            filters = DocumentSearchFilters()

        builded_filters = {}
        
        if filters.city:
            if isinstance(filters.city, list):
                builded_filters["city"] = {"$in": filters.city}
            else:
                builded_filters["city"] = filters.city
        
        if filters.state:
            if isinstance(filters.state, list):
                builded_filters["state"] = {"$in": filters.state}
            else:
                builded_filters["state"] = filters.state

        query_vector = self.embedding_model.encode(
            query
        )  # Encode the query string to a vector
        results: QueryResponse = self.index.query(
            query_vector, top_k=10, include_metadata=True, filter=builded_filters
        )

        documents: List[Document] = []
        for r in results.matches:
            doc = r.metadata
            doc["score"] = r.score
            documents.append(Document(**doc))
        return documents

    def split_into_batches(self, input_array, batch_size):
        """
        Split an array into batches of a specified size.

        Args:
            input_array (list or array-like): The array to split.
            batch_size (int): The batch size for splitting.

        Returns:
            List of batches.
        """
        return [
            input_array[i : i + batch_size]
            for i in range(0, len(input_array), batch_size)
        ]

    def insert_many(self, documents: List[Document]):
        items = []
        for doc in documents:
            vector = self.generate_vector(doc)
            _id = self.generate_id(doc)
            record: EmbeddingDocument = EmbeddingDocument(
                id=_id, values=vector, metadata=doc
            )
            items.append(record.model_dump())

        # Upsert data with 100 vectors per upsert request
        for ids_vectors_chunk in self.split_into_batches(items, batch_size=25):
            print(f"Insert to Storage {len(ids_vectors_chunk)} documents")
            self.index.upsert(
                vectors=ids_vectors_chunk
            )  # Assuming `index` defined elsewhere

    def generate_vector(self, doc):
        return self.embedding_model.encode(
            doc.title + doc.description + doc.full_location
        )
