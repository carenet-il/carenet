import os
from typing import List

from libs.embedding.cohere_multilingual_embedding import CohereMultilingualEmbedding
from libs.feed.btl_anxiety_feed import BtlAnxietyFeed
from libs.feed.extractors.extractors import extract_best_match, insert_geo_loc_to_doc
from libs.feed.moh_mentalHeltahClinics_feed import MOH_MentalHealthClinicsFeed
from libs.feed.moh_resilienceCenters_feed import MOH_ResilienceCentersFeed
from libs.feed.n12_feed import N12Feed
from libs.feed.nafshi_feed import NafshiFeed
from libs.feed.btl_all_regions_feed import BtlFeed
from libs.feed.otef_lev_feed import OtefLevFeed
from libs.interfaces.document import Document
from libs.vector_storage import VectorStorage
from libs.vector_storage.vector_provider.mongodb import MongoVectorProvider



def main():
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

    feeds = [n12_feed, nafshi_feed, minster_of_health_resilience_centers_feed, btl_all_regions_feed, btl_anxiety_feed,otef_lev_feed,minster_of_health_mental_clinic]
 
    for feed in feeds:
        norm_documents: List[Document] = feed.pull()
                
        '''' 
        edge-case:
        check if the class name of the current feed object matches 'NafshiFeed'
        because the geo-location is insert inside the nafshi_feed.py file.
        # todo : this part can be remove and put a city inside nafshi with the extract_best_match
        '''
        if feed.__class__.__name__ == "NafshiFeed":
            vector_storage.insert_documents(norm_documents=norm_documents)
        else:
            # normalize each city in each doc
            norm_documents_city_normalize = extract_best_match(norm_documents)

            # adding to each doc his geo-location based on city name
            norm_documents_geo_city_normalize = insert_geo_loc_to_doc(norm_documents_city_normalize)
            vector_storage.insert_documents(norm_documents=norm_documents_geo_city_normalize)
                
        vector_storage.insert_documents(norm_documents=norm_documents)

    print("done feeds crawler")

if __name__ == "__main__":
    main()
