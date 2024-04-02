import os
from typing import List
from libs.embedding.cohere_multilingual_embedding import CohereMultilingualEmbedding
from libs.feed.btl_anxiety_feed import BtlAnxietyFeed
from libs.feed.geo_location.geo_location_utils import insert_location_object_to_documents_by_city_or_state, \
    get_cities_israel_heb
from libs.feed.maccabi_therapy_feed import MaccabiTherapyClinicsFeed
from libs.feed.moh_mental_healthClinics_feed import MOH_MentalHealthClinicsFeed
from libs.feed.moh_resilienceCenters_feed import MOH_ResilienceCentersFeed
from libs.feed.n12_feed import N12Feed
from libs.feed.nafshi_feed import NafshiFeed
from libs.feed.btl_all_regions_feed import BtlFeed
from libs.feed.normalize.normalize_utils import normalize_cities
from libs.feed.otef_lev_feed import OtefLevFeed
from libs.interfaces.document import Document
from libs.vector_storage import VectorStorage
from libs.vector_storage.vector_provider.mongodb import MongoVectorProvider
import sys, os
from dotenv import load_dotenv


def main():
    load_dotenv()
    # to allow import from libs
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

    embedding_model = CohereMultilingualEmbedding()

    storage_provider = MongoVectorProvider(mongodb_uri=os.getenv("MONGO_URI"),
                                           embedding_model=embedding_model, db_name="dev")

    vector_storage = VectorStorage(storage_provider=storage_provider)

    # feeds
    n12_feed = N12Feed()
    nafshi_feed = NafshiFeed()
    minster_of_health_resilience_centers_feed = MOH_ResilienceCentersFeed()
    btl_all_regions_feed = BtlFeed()
    btl_anxiety_feed = BtlAnxietyFeed()
    otef_lev_feed = OtefLevFeed()
    minster_of_health_mental_clinic = MOH_MentalHealthClinicsFeed()
    maccabi_feed = MaccabiTherapyClinicsFeed()

    feeds = [n12_feed, nafshi_feed, minster_of_health_resilience_centers_feed, btl_all_regions_feed, btl_anxiety_feed,otef_lev_feed,minster_of_health_mental_clinic,maccabi_feed]
    # For dynamic list and updated
    cities_israel_heb = get_cities_israel_heb()
    for feed in feeds:
        norm_documents: List[Document] = feed.pull()

        # normalize each city in each doc
        norm_documents_city_normalize = normalize_cities(cities_israel_heb, norm_documents)
        # adding to each doc his geolocation based on city name
        norm_documents_included_location = insert_location_object_to_documents_by_city_or_state(
            norm_documents_city_normalize)
        vector_storage.insert_documents(norm_documents=norm_documents_included_location)

    print("done feeds crawler")


if __name__ == "__main__":
    main()
