from abc import ABC
from typing import List, Optional

from pymongo import MongoClient, UpdateOne
from pymongo.errors import PyMongoError

from libs.embedding.abstract import EmbeddingAbstract
from libs.feed.geo_location.geo_location_utils import (
    extract_geo_loc_from_city,
    get_cities_israel_heb,
)
from libs.interfaces.document import Document, EmbeddingDocument, DocumentSearchFilters
from libs.interfaces.locations import IsraelRegions
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

        latitude = None
        longitude = None
        # Filter by city with radius or by state only support
        if filters.city and isinstance(filters.city, str) and filters.radius:
            latitude, longitude = extract_geo_loc_from_city(filters.city)

        elif filters.state:
            if isinstance(filters.state, str):
                filters.state = [filters.state]
            if filters.include_remote:
                filters.state.append(IsraelRegions.NATIONAL.value)
                
            built_filters.append({"metadata.state": {"$in": filters.state}})

        # Audience filter setup
        if filters.audience:
            if isinstance(filters.audience, list):
                built_filters.append({"metadata.audience": {"$in": filters.audience}})
            else:
                built_filters.append({"metadata.audience": filters.audience})

        query_vector = self.embedding_model.encode(
            query
        )  # Encode the query string to a vector

        if len(query_vector) == 0:
            return []

        documents_in_the_area = []
        if latitude is not None and longitude is not None and filters.radius > 0:
            documents_in_the_area = self.get_documents_in_the_area(
                longitude, latitude, filters.radius
            )

        if len(documents_in_the_area) > 0:
            if filters.include_remote:
                built_filters.append({
                    "$or": [
                        {"id": {"$in": documents_in_the_area}},
                        {"metadata.state": IsraelRegions.NATIONAL.value}
                    ]
                })
            else:
                built_filters.append({"id": {"$in": documents_in_the_area}})
                
        pipelines = [
            {
                "$vectorSearch": {
                    "index": "default_vector_index",
                    "path": "values",
                    "filter": ({"$and": built_filters} if built_filters else None),
                    "queryVector": query_vector,
                    "numCandidates": k,
                    "limit": k // 10,
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

        results = self.document_collection.aggregate(pipelines)

        return [Document(**doc) for doc in results]

    def delete_all(self):
        try:
            deleted_docs = self.document_collection.delete_many({})
            if deleted_docs.deleted_count > 0:
                print("Deleted all documents from the collection successfully.")
            else:
                print("No documents found to delete.")
        except PyMongoError as e:
            print(f"An error occurred while deleting documents: {e}")

    def insert_many(self, documents: List[Document]):
        operations = []

        for doc in documents:
            doc.id = self.generate_id(doc)

        ids_db = set(self.document_collection.distinct("id"))

        documents = list(filter(lambda _doc: _doc.id not in ids_db, documents))

        print(f"document insert now {len(documents)}")

        if len(documents) == 0:
            return

        vectors = self.generate_vector_bulk(documents)

        for i, doc in enumerate(documents):
            vector = vectors[i]
            # Prepare the update operation instead of creating a new document

            record: EmbeddingDocument = EmbeddingDocument(
                id=doc.id, values=vector, metadata=doc
            )

            operation = UpdateOne(
                {"id": record.id},  # Filter document by _id
                {"$set": record.model_dump()},  # Update these fields
                upsert=True,  # Perform an insert if the document does not exist
            )
            operations.append(operation)

        # Perform bulk write operation with upsets
        if operations:  # Check if the list is not empty
            self.document_collection.bulk_write(operations)

    def generate_vector_text(self, doc: Document):
        return " ".join(
            [doc.title, doc.description, " ".join(doc.audience), doc.city, doc.state]
        )

    def generate_vector_bulk(self, documents: List[Document]) -> List[List[float]]:
        titles = list(map(lambda doc: self.generate_vector_text(doc), documents))

        # Function to chunk the titles list into batches of 25
        def chunker(seq, size):
            return (seq[pos : pos + size] for pos in range(0, len(seq), size))

        vectors = []  # Initialize an empty list to store the encoded vectors
        for chunk in chunker(titles, 100):
            # Encode each chunk and extend the vectors list with the results
            vectors.extend(self.embedding_model.encode_bulk(chunk))

        return vectors

    def fetch_search_filters(self) -> DocumentSearchFilters:

        cities = get_cities_israel_heb()

        states = self.document_collection.distinct(
            "metadata.state", {"metadata.state": {"$nin": [None, ""]}}
        )

        audiences = self.document_collection.distinct(
            "metadata.audience", {"metadata.audience": {"$nin": [None, ""]}}
        )

        return DocumentSearchFilters(city=cities, state=states, audience=audiences)

    def get_documents_in_the_area(self, longitude, latitude, radius):

        pipeline = [
            {
                "$geoNear": {
                    "near": {"type": "Point", "coordinates": [longitude, latitude]},
                    "distanceField": "dist.calculated",
                    "maxDistance": radius,
                    "includeLocs": "dist.location",
                    "spherical": True,
                }
            },
            {"$project": {"id": 1}},
        ]

        results = self.document_collection.aggregate(pipeline)

        return list(map(lambda r: r["id"], results))
