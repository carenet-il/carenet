from abc import ABC
from typing import List, Optional

from pymongo import MongoClient

from libs.embedding.abstract import EmbeddingAbstract
from libs.interfaces.document import Document, EmbeddingDocument, DocumentSearchFilters
from libs.vector_storage.vector_provider.abstract import VectorProviderAbstract


class MongoVectorProvider(VectorProviderAbstract, ABC):
    
    def __init__(
        self,
        embedding_model: EmbeddingAbstract,
        db_name: str,
        mongodb_uri: str = "mongodb://localhost:27017/",
    ):

        self.client = MongoClient(mongodb_uri)
        self.db = self.client[db_name]
        self.document_collection = self.db["documents"]
        super().__init__(embedding_model)
    
    def search(
        self,
        query: str,
        filters: Optional[DocumentSearchFilters] = None,
        k: int = 100,
        threshold: float = 0.9,
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

        documents: List[Document] = []

        if len(query_vector) == 0:
            return documents

        results: QueryResponse = self.index.query(
            query_vector, top_k=k, include_metadata=True, filter=builded_filters
        )

        for r in results.matches:
            if r.score >= threshold:
                doc = r.metadata
                doc["score"] = r.score
                documents.append(Document(**doc))
        return documents

    def delete_all(self):
        self.index.delete(delete_all=True, namespace="")

    def insert_many(self, documents: List[Document]):
        items = []
        for doc in documents:
            vector = self.generate_vector(doc)
            _id = self.generate_id(doc)
            record: EmbeddingDocument = EmbeddingDocument(
                id=_id, values=vector, metadata=doc
            )
            items.append(record.model_dump())

        self.document_collection.insert_many(items)

    def generate_vector(self, doc: Document):
        return self.embedding_model.encode(doc.title)

    def fetch_search_filters(self) -> DocumentSearchFilters:
        res = self.index.query(
            vector=[0] * 768,
            # this is the max value for top_k
            top_k=10000,
            include_metadata=True,
            include_values=False,
            filter={
                "$or": [
                    {Document.Fields.city: {"$exists": True}},
                    {Document.Fields.state: {"$exists": True}},
                ]
            },
        )

        cities = set()
        states = set()

        for r in res.matches:
            metadata = r.metadata
            if Document.Fields.city in metadata:
                value = metadata[Document.Fields.city]
                if value:
                    cities.add(value)
            if Document.Fields.state in metadata:
                value = metadata[Document.Fields.state]
                if value:
                    states.add(value)

        return DocumentSearchFilters(city=list(cities), state=list(states))
