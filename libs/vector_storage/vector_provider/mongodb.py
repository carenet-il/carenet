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

        builded_filters = []

        if filters.city:
            if isinstance(filters.city, list):
                builded_filters.append({"metadata.city": {"$in": filters.city}})
            else:
                builded_filters.append({"metadata.city": filters.city})

        if filters.state:
            if isinstance(filters.state, list):
                builded_filters.append({"metadata.state": {"$in": filters.state}})
            else:
                builded_filters.append({"metadata.state": filters.state})

        query_vector = self.embedding_model.encode(
            query
        )  # Encode the query string to a vector

        if len(query_vector) == 0:
            return []

        results = self.document_collection.aggregate(
            [
                {
                    "$vectorSearch": {
                        "index": "default_vector_index",
                        "path": "values",
                        "filter": (
                            {"$and": builded_filters} if builded_filters else None
                        ),
                        "queryVector": query_vector,
                        "numCandidates": k * 10,
                        "limit": k,
                    }
                },
                {"$addFields": {"score": {"$meta": "vectorSearchScore"}}},
                # {"$match": {"score": {"$gte": threshold}}},
                {"$sort": {"score": -1}},
                {
                    "$replaceRoot": {
                        "newRoot": {"$mergeObjects": ["$metadata", {"score": "$score"}]}
                    }
                },
            ]
        )

        return list(results)

    def delete_all(self):
        self.document_collection.delete_many({})

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

        cities = self.document_collection.distinct("metadata.city", {"metadata.city": {"$nin": [None, ""]}})

        states = self.document_collection.distinct("metadata.state", {"metadata.state": {"$nin": [None, ""]}})

        return DocumentSearchFilters(city=cities, state=states)
