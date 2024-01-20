import os

from libs.embedding.quora_distilbert_multilingual_embedding import (
    QuoraDistilBertMultilingualEmbedding,
)
from libs.vector_storage import VectorStorage
from libs.vector_storage.vector_provider.pincone_vector_provider import (
    PineconeVectorProvider,
)

embedding_model = QuoraDistilBertMultilingualEmbedding(load_locally_model=False)

storage_provider = PineconeVectorProvider(
    embedding_model=embedding_model,
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT"),
    index_name=os.getenv("PINECONE_INDEX_NAME"),
)

vector_storage = VectorStorage(storage_provider=storage_provider)
