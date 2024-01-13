from libs.embedding.quora_distilbert_multilingual_embedding import (
    QuoraDistilBertMultilingualEmbedding,
)
from libs.vector_storage.vector_provider.pincone_vector_provider import (
    PineconeVectorProvider,
)
from libs.vector_storage import VectorStorage
import os

embedding_model = QuoraDistilBertMultilingualEmbedding()

storage_provider = PineconeVectorProvider(
    embedding_model=embedding_model,
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT"),
    index_name=os.getenv("PINECONE_INDEX_NAME"),
)

vector_storage = VectorStorage(storage_provider=storage_provider)
