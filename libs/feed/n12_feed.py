from abc import ABC
from typing import List

import requests

from libs.feed.abstract.feed_abstract import FeedAbstract, get_location
from libs.interfaces.document import Document, SourceType


class N12Feed(FeedAbstract, ABC):
    def pull(self) -> List[Document]:
        url = "https://map-app.mappo.world:5000/fetch?app_id=0&event_type=offer_help&subcat_id=98"

        payload = {}
        headers = {
            'authority': 'map-app.mappo.world:5000',
            'accept': '/',
            'accept-language': 'en,en-US;q=0.9,he;q=0.8',
            'origin': 'https://map-fe.mappo.world',
            'referer': 'https://map-fe.mappo.world/',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        records = response.json()

        documents: List[Document] = [self.__norm_document__(doc) for doc in records]

        return documents

    """
    {
            "item_id": 54,
            "event_type": "offer_help",
            "header": "Cynet",
            "address": "",
            "content": "<p style=\"text-align: right;\">החברה מציעה לתושבי הדרום לינה במשרדי החברה ושימוש בכלל מתקני המשרד כולל מתן תרופות ואוכל.</p>",
            "contact_name": null,
            "contact_email": null,
            "contact_phone": "0546695004",
            "external_link": null,
            "report_link": null,
            "is_active": 1,
            "subcats": [
                {
                    "id": 35,
                    "name": "דירה"
                }
            ],
            "apps": [
                {
                    "id": 1,
                    "name": "ynet",
                    "domain": "ynet.co.il"
                }
            ],
            "cat": {
                "id": 3,
                "name": "מגורים"
            },
            "location": {
                "lat": 31.949646,
                "lon": 34.8030548
            }
        }
    """

    def __norm_document__(self, document) -> Document:
        document_dict = {
            "title": document["header"],
            "description": document["content"],
            "email": document["contact_email"],
            "phone_number": document["contact_phone"],
            "source": SourceType.N12,
            "location": get_location(document["location"]["lat"], document["location"]["lon"])
        }

        return Document(**document_dict)
