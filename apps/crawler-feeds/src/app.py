import os
from typing import List

from libs.embedding.quora_distilbert_multilingual_embedding import QuoraDistilBertMultilingualEmbedding
from libs.feed.btl_anxiety_feed import BtlAnxietyFeed
from libs.feed.mental_health_clinics_moh_feed import MhcFeed
from libs.feed.n12_feed import N12Feed
from libs.feed.nafshi_feed import NafshiFeed
from libs.feed.btl_all_regions_feed import BtlFeed
from libs.feed.otef_lev_feed import OtefLevFeed
from libs.interfaces.document import Document
from libs.vector_storage import VectorStorage
from libs.vector_storage.vector_provider.pincone_vector_provider import PineconeVectorProvider


def main():
    embedding_model = QuoraDistilBertMultilingualEmbedding(load_locally_model=True)

    storage_provider = PineconeVectorProvider(embedding_model=embedding_model, api_key=os.getenv("PINECONE_API_KEY"),
                                              environment=os.getenv("PINECONE_ENVIRONMENT"),
                                              index_name=os.getenv("PINECONE_INDEX_NAME"))

    vector_storage = VectorStorage(storage_provider=storage_provider)
    
    # feeds
    n12_feed = N12Feed()
    nafshi_feed = NafshiFeed()
    minster_of_health_feed = MhcFeed()
    btl_all_regions_feed = BtlFeed()
    btl_anxiety_feed = BtlAnxietyFeed()
    otef_lev_feed = OtefLevFeed()

    feeds = [n12_feed, nafshi_feed, minster_of_health_feed, btl_all_regions_feed, btl_anxiety_feed,otef_lev_feed, ]

    for feed in feeds:
        norm_documents: List[Document] = feed.pull()
        vector_storage.insert_documents(norm_documents=norm_documents)


if __name__ == "__main__":
    main()
