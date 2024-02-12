from abc import ABC
from typing import List, Optional

from pymongo import MongoClient, UpdateOne

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

        built_filters = []

        if filters.city:
            if isinstance(filters.city, list):
                built_filters.append({"metadata.city": {"$in": filters.city}})
            else:
                built_filters.append({"metadata.city": filters.city})

        if filters.state:
            if isinstance(filters.state, list):
                built_filters.append({"metadata.state": {"$in": filters.state}})
            else:
                built_filters.append({"metadata.state": filters.state})

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
                            {"$and": built_filters} if built_filters else None
                        ),
                        "queryVector": query_vector,
                        "numCandidates": k,
                        "limit": k // 10
                    }
                },
                {"$addFields": {"score": {"$meta": "vectorSearchScore"}}},
                {"$match": {"score": {"$gte": threshold}}},
                {"$sort": {"score": -1}},
                {
                    "$replaceRoot": {
                        "newRoot": {"$mergeObjects": ["$metadata", {"score": "$score"}]}
                    }
                },
            ]
        )

        return [Document(**doc) for doc in results]

    def delete_all(self):
        self.document_collection.delete_many({})

    def insert_many(self, documents):
        operations = []
        for doc in documents:
            vector = self.generate_vector(doc)
            _id = self.generate_id(doc)
            # Prepare the update operation instead of creating a new document

            record: EmbeddingDocument = EmbeddingDocument(
                id=_id, values=vector, metadata=doc)

            operation = UpdateOne(
                {'id': record.id},  # Filter document by _id
                {'$set': record.model_dump()},  # Update these fields
                upsert=True  # Perform an insert if the document does not exist
            )
            operations.append(operation)

        # Perform bulk write operation with upsets
        if operations:  # Check if the list is not empty
            self.document_collection.bulk_write(operations)

    def generate_vector(self, doc: Document):
        return self.embedding_model.encode(doc.title)

    def fetch_search_filters(self) -> DocumentSearchFilters:

        cities = self.document_collection.distinct("metadata.city", {"metadata.city": {"$nin": [None, ""]}})

        states = self.document_collection.distinct("metadata.state", {"metadata.state": {"$nin": [None, ""]}})

        return DocumentSearchFilters(city=cities, state=states)
