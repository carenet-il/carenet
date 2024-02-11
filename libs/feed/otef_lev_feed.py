from abc import ABC
import requests
from libs.feed.abstract import FeedAbstract

from libs.interfaces.document import Document, SourceType
from libs.feed.extractors.extractors import extract_region_by_city,join_elements_with_separator

class OtefLevFeed(FeedAbstract, ABC):

    def pull(self) -> list[Document]:
        
        documants: list[Document] = []
        
        url = 'https://www.oteflev.org.il/_api/cloud-data/v1/wix-data/collections/query'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'authorization': 'wixcode-pub.d6ce8df90162cb24476388b603170b4c1b03ff22.eyJpbnN0YW5jZUlkIjoiZjAyOGNlNzQtOTAxZi00YzI0LTg1MzMtYmQ4MDFlZDRhOTRlIiwiaHRtbFNpdGVJZCI6ImEzMDVhYmE3LTkwODItNGYwYi05OWFmLTA2MGMyYjc5MTA2ZSIsInVpZCI6bnVsbCwicGVybWlzc2lvbnMiOm51bGwsImlzVGVtcGxhdGUiOmZhbHNlLCJzaWduRGF0ZSI6MTcwNzU4MjY1NTE5OSwiYWlkIjoiNDA4ODY4OTEtZmVjYi00MDgzLWEzMzEtYTE4NDEzMjhhYjVjIiwiYXBwRGVmSWQiOiJDbG91ZFNpdGVFeHRlbnNpb24iLCJpc0FkbWluIjpmYWxzZSwibWV0YVNpdGVJZCI6IjkzYmY5ZGZjLTk5N2QtNDMzMC05MGYyLTE5NTU5NTUyN2QxZSIsImNhY2hlIjpudWxsLCJleHBpcmF0aW9uRGF0ZSI6bnVsbCwicHJlbWl1bUFzc2V0cyI6IlNob3dXaXhXaGlsZUxvYWRpbmcsSGFzRG9tYWluLEFkc0ZyZWUiLCJ0ZW5hbnQiOm51bGwsInNpdGVPd25lcklkIjoiNDZjOGExZWYtOTQxMC00NGRkLTgzMmQtNTQ4MTMyNmZhZTUxIiwiaW5zdGFuY2VUeXBlIjoicHViIiwic2l0ZU1lbWJlcklkIjpudWxsLCJwZXJtaXNzaW9uU2NvcGUiOm51bGwsImxvZ2luQWNjb3VudElkIjpudWxsLCJpc0xvZ2luQWNjb3VudE93bmVyIjpudWxsfQ==',
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.oteflev.org.il/_partials/wix-thunderbolt/dist/clientWorker.9af24196.bundle.min.js',
            'commonConfig': '%7B%22brand%22%3A%22studio%22%2C%22host%22%3A%22VIEWER%22%2C%22BSI%22%3A%22c88f98dc-20db-4d95-84cb-5674a83872c6%7C2%22%7D',
            'x-wix-brand': 'studio',
            'X-Wix-Client-Artifact-Id': 'wix-thunderbolt'
        }

        offset = 0
        limit = 25

        data = {
            "collectionName": "services",
            "dataQuery": {
                "filter": {
                    "public": {"$eq": True},
                    "city": {
                        "$hasSome": ["אופקים", "אילת", "ארצי", "בת ים", "גולן", "ירושלים", "ים המלח", "טבריה", "הרצליה", "חיפה",
                                    "נתניה", "מצפה רמון", "כללי", "ירושלים ומבואות ירושלים", "סובב כנרת", "עמק הירדן",
                                    "עמק יזרעאל", "ערבה", "רמת נגב", "קרית שמונה", "ערד", "ערבה תיכונה", "תל אביב"]},
                    "Residence": {
                        "$hasSome": ["כל הארץ", "חוף אשקלון", "אשקלון", "אשכול", "כלל המפונים במרכז המפונים", "מ.א גליל עליון",
                                    "מעלה יוסף", "מטולה", "מטה אשר", "מ.א מבוא חרמון", "קריית שמונה", "קרית שמונה", "שדות נגב",
                                    "שדרות", "שער הנגב", "שלומי"]}
                },
                "paging": {"offset": offset, "limit": limit},
                "fields": ['title', 'city', 'subExperty', 'contact', 'ages', 'location', 'workingHours', ]
            },
            "options": {},
            "includeReferencedItems": [],
            "segment": "LIVE",
            "appId": "c25de19e-ffc4-4e24-b6d2-f09b2abf75ea"
        }

        while True:
            # fetch the page
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
            
            # Iterate through each item in the 'items' list
            for doc in response_data['items']:
                cities = doc.get('city') # get's all the cities, mose of the time there is more than 1
                for city in cities:
                    doc['city'] = city # call __norm_document__ with a spesfic city
                    documants.append(self.__norm_document__(doc))

            # update offset and limit for the next page
            offset += len(response_data['items'])
            if offset >= response_data['totalCount']:
                break

            data["dataQuery"]["paging"]["offset"] = offset  # update and offset

        print(f'number of documants in Otef Lev is {len(documants)}')
        print(f'documants - {documants}')
        
        return documants

    def __norm_document__(self,document) -> Document:
        
        # get all the expertises from the list
        expertises = join_elements_with_separator(document.get('experty', ''))

        # get all the ages from the list
        ages = join_elements_with_separator(document.get('ages', ''))
        
        document_dict = {
            "title": document.get('title', ''),
            "description": f'{expertises} {ages}',
            "phone_number": document.get("contact", ''),
            "source": SourceType.OTEFLEV.name,
            "full_location": f"{document.get('location', '')} {document.get('workingHours', '')}",
            "city": document.get('city',''),
            "state": extract_region_by_city(document.get('city','')),
        }

        return Document(**document_dict)



