from abc import ABC
import requests
from libs.feed.abstract import FeedAbstract
from libs.interfaces.document import Document, SourceType
from libs.feed.extractors.extractors import extract_region_from_city


class MOH_ResilienceCentersFeed(FeedAbstract, ABC):
    
    def pull(self) -> list[Document]:

        # get the number of records from the db of Mental Help Centers
        num_of_records = requests.get(
        'https://services5.arcgis.com/dlrDjz89gx9qyfev/arcgis/rest/services/Mental_Help_Centers/FeatureServer/0/query?f=json&where=1%3D1&returnCountOnly=true')

        # extract the number of records in the db
        number_of_records = num_of_records.json().get('count')

        # fetching all records up to the specified limit from the Mental Help Centers dataset
        response = requests.get(
            f'https://services5.arcgis.com/dlrDjz89gx9qyfev/arcgis/rest/services/Mental_Help_Centers/FeatureServer/0/query?f=json&cacheHint=true&resultOffset=0&resultRecordCount={number_of_records}&where=1%3D1&orderByFields=institute_desc%20ASC&outFields=*&resultType=standard&returnGeometry=false&spatialRel=esriSpatialRelIntersects')
        
        records = response.json()

        # records.get('features') is a list
        documents: list[Document] = [self.__norm_document__(doc) for doc in records.get('features')]

        print(f'Found at minister of health resilience centers {len(documents)} documents')
        return documents

    def __norm_document__(self, document) -> Document:

        record = document.get('attributes')
        city = record.get('CityName', "")

        document_dict = {
            "title": record.get("institute_desc", ""),
            "description": record.get("institute_type_desc", ""),
            "phone_number": record.get("Phone", ""),
            "source": SourceType.MOH.name, # MOH stands for Ministry of Health
            "full_location": record.get('Address', ""),
            "city": city,
            "state": extract_region_from_city(city), # the function returns an empty string if not found
        }

        return Document(**document_dict)