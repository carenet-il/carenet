from typing import List

from libs.embedding.minilmv6_embedding import MiniLMv6Embedding
from libs.feed.n12_feed import N12Feed
from libs.interfaces.document import Document
from libs.vector_storage.vector_provider.pincone_vector_provider import PineconeVectorProvider
from libs.vector_storage.vector_storage import VectorStorage


def main():
    embedding_model = MiniLMv6Embedding()
    storage_provider = PineconeVectorProvider(embedding_model=embedding_model)

    vector_storage = VectorStorage(storage_provider=storage_provider)
    n12_feed = N12Feed()

    feeds = [n12_feed]

    for feed in feeds:
        norm_documents: List[Document] = feed.pull()
        vector_storage.insert_documents(norm_documents=norm_documents)


if __name__ == "__main__":
    main()
