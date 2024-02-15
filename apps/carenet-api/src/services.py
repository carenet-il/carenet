import os

from libs.embedding.cohere_multilingual_embedding import CohereMultilingualEmbedding

from libs.vector_storage import VectorStorage
from libs.vector_storage.vector_provider.mongodb import MongoVectorProvider

embedding_model = CohereMultilingualEmbedding()

storage_provider = MongoVectorProvider(
    embedding_model=embedding_model,
    db_name="dev",
    mongodb_uri=os.getenv("MONGO_URI"),
)

vector_storage = VectorStorage(storage_provider=storage_provider)
