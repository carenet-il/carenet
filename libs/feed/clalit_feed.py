from abc import ABC
import json
import requests
from libs.feed.abstract import FeedAbstract

from libs.feed.normalize.normalize_utils import normalize_telephones, normalize_treatments
from libs.interfaces.document import Document, SourceType


class ClalitFeed(FeedAbstract, ABC):

    def pull(self) -> list[Document]:

        documents: list[Document] = []
        
        url = 'https://apps.clalit.co.il/SupplierDataRESTService/api/supplier/GetJsonGroupSearchBody'

        body_data = {
            "serviceID": "33-0",
            "reqApplication": 103,
            "cityID": None,
            "operationId": None,
            "xMap": None,
            "yMap": None,
            "specialtyID": None,
            "treatmentID": None
        }
        
        response = requests.post(url, json=body_data)

        data = json.loads(response.json())
        suppliers_list = data.get("Suppliers", {}).get("SuppliersList", [])

        for supplier in suppliers_list:
            doc = {}

            doc['audience'] = ['ילדים ונוער']
            doc['title'] = supplier.get("PlaceName", "")
            doc['city'] = supplier.get("CityName", "")
            doc['full_location'] = supplier.get("Address", "")
            doc['telephone'] = normalize_telephones(supplier)
            doc['treatments'] = normalize_treatments(supplier)

            documents.append(self.__norm_document__(doc))
        
        print(f'ClalitFeed: {len(documents)} documents were pulled')
        return documents

    def __norm_document__(self, document: dict) -> Document:

        document_dict = {
                "title": document.get('title', ''),
                "description": document.get('treatments'),
                "phone_number": document.get('telephone', ''),
                "source": SourceType.CLALIT.name,
                "city": document.get('city', ''),
                "audience": document.get('audience', ''),
        }

        return Document(**document_dict)
