import json
from abc import ABC
from typing import List, Optional

import requests
from pydantic import BaseModel, Field

from libs.feed.abstract import FeedAbstract
from libs.feed.extractors.extractors import extract_audience_from_doc
from libs.interfaces.document import Document, SourceType

nafshi_to_genral_region = {
    "איו״ש": "מחוז ירושלים",
    "ארצי - מרחוק": "ארצי - מרחוק",
    "דרום - נגב צפוני": "מחוז הדרום",
    "המרכז": "מחוז המרכז",
    "השרון": "מחוז המרכז",
    "ירושלים והסביבה": "מחוז ירושלים",
    "ישובי העוטף": "מחוז הדרום",
    "מרכז": "מחוז תל אביב",
    "צפון": "מחוז הצפון",
    "שפלה": "מחוז המרכז"
}


class NafshiDocument(BaseModel):
    tagsAges: Optional[List[str]] = []
    serviceOrientationTags: Optional[List[str]] = []
    serviceName: str = Field(...)
    organizationName: Optional[str] = ''
    serviceLink: Optional[str] = ''
    phoneNumber: Optional[str] = ''
    langsTags: Optional[List[str]] = []
    serviceDescription: Optional[str] = ''
    location1: Optional[List[str]] = ''
    tagsPopulationType: Optional[List[str]] = []
    targetAudienceTags: Optional[List[str]] = []


class NafshiFeed(FeedAbstract, ABC):
    def pull(self) -> List[Document]:
        url = "https://www.nafshi.info/_api/cloud-data/v1/wix-data/collections/query"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'authorization': 'wixcode-pub.cc2123599de93ff1c6d2e75fc47b0462f737630d.eyJpbnN0YW5jZUlkIjoiZDcyMTQyOTktY2VjZC00YzE0LTg1ZDAtNDM4NGFhZmMyMTU4IiwiaHRtbFNpdGVJZCI6IjA3MWFiZTk1LTc0N2YtNDAwZS04NzljLTFmMTQ1NDZiMjMwNSIsInVpZCI6bnVsbCwicGVybWlzc2lvbnMiOm51bGwsImlzVGVtcGxhdGUiOmZhbHNlLCJzaWduRGF0ZSI6MTcwNjM0NjY0ODg2OSwiYWlkIjoiMTk2MTAxYTktOTBhMi00ZGVjLWI3NDktNjhkZThlYzc4ZTA5IiwiYXBwRGVmSWQiOiJDbG91ZFNpdGVFeHRlbnNpb24iLCJpc0FkbWluIjpmYWxzZSwibWV0YVNpdGVJZCI6ImFmNGFmM2JiLTY1OTEtNDcxNy04ZTA1LWUwNDIxYWFhOTZmYyIsImNhY2hlIjpudWxsLCJleHBpcmF0aW9uRGF0ZSI6bnVsbCwicHJlbWl1bUFzc2V0cyI6Ikhhc0RvbWFpbixTaG93V2l4V2hpbGVMb2FkaW5nLEFkc0ZyZWUiLCJ0ZW5hbnQiOm51bGwsInNpdGVPd25lcklkIjoiMTJkZGNmYWMtOTFmNC00MDU0LTg1ODEtMGM0ZDBiNzgxZjFmIiwiaW5zdGFuY2VUeXBlIjoicHViIiwic2l0ZU1lbWJlcklkIjpudWxsLCJwZXJtaXNzaW9uU2NvcGUiOm51bGwsImxvZ2luQWNjb3VudElkIjpudWxsLCJpc0xvZ2luQWNjb3VudE93bmVyIjpudWxsfQ==',
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.nafshi.info/_partials/wix-thunderbolt/dist/clientWorker.cd27c35d.bundle.min.js',
            'commonConfig': '%7B%22brand%22%3A%22studio%22%2C%22host%22%3A%22VIEWER%22%2C%22BSI%22%3A%2266768b87-4d01-4a28-b923-19af142e356e%7C1%22%7D',
            'x-wix-brand': 'studio',
            'X-Wix-Client-Artifact-Id': 'wix-thunderbolt',
            'Cookie': 'XSRF-TOKEN=1706346704|LCwoAI8tO6Ss'
        }

        nafshi_documents: list[NafshiDocument] = []

        chunk_size = 12

        payload = {
            "collectionName": "JDCv3",
            "dataQuery": {
                "filter": {},
                "sort": [
                    {
                        "fieldName": "_updatedDate",
                        "order": "DESC"
                    }
                ],
                "paging": {
                    "offset": 0,
                    "limit": chunk_size
                },
                "fields": []
            },
            "options": {},
            "includeReferencedItems": [],
            "segment": "LIVE",
            "appId": "0e394bc2-134b-43f1-98fe-e62f71457063"
        }

        payload_dumps = json.dumps(payload)

        response = requests.request("POST", url, headers=headers, data=payload_dumps)
        records = response.json()
        nafshi_documents = nafshi_documents + list(map(lambda x: NafshiDocument(**x), records["items"]))

        while records["pagingMetadata"]["hasNext"]:
            payload["dataQuery"]["paging"]["offset"] += payload["dataQuery"]["paging"]["limit"]
            payload_dumps = json.dumps(payload)
            response = requests.request("POST", url, headers=headers, data=payload_dumps)
            records = response.json()
            nafshi_documents = nafshi_documents + list(map(lambda x: NafshiDocument(**x), records["items"]))

        print(f"found at Nafshi {len(nafshi_documents)} documents")

        norm_documents: List[Document] = []
        for doc in nafshi_documents:
            norm_results = self.__norm_document__(doc)
            norm_documents = norm_documents + norm_results

        return norm_documents

    def __norm_document__(self, document: NafshiDocument) -> List[Document]:
        documents_final: List[Document] = []

        description = f"""
            {document.organizationName}
            {document.serviceDescription}   
            {",".join(document.targetAudienceTags)}  
            {",".join(document.tagsAges)}  
            {",".join(document.tagsPopulationType)}
            {",".join(document.serviceOrientationTags)} 
            {",".join(document.langsTags)} 
            """
            
        # extract the audiences from the doc, can be : צעירים מבוגרים אזרחים ותיקים in one doc and we only have to filters for ages
        audiences = []
        for age in document.tagsAges:
            audience_candidate = extract_audience_from_doc(age)
            if audience_candidate in audiences:
                continue
            audiences.append(audience_candidate)
                

        if type(document.location1) == list:
            for location in document.location1:
                # state is the region of this record
                state = nafshi_to_genral_region.get(location, "")

                document_dict = {
                    "title": document.organizationName + " " + document.serviceName,
                    "description": description,
                    "phone_number": document.phoneNumber,
                    "source": SourceType.NAFSHI.name,
                    "website": document.serviceLink,
                    "state": state,
                    "audience": audiences
                }
                
                documents_final.append(Document(**document_dict))
                print(Document(**document_dict))

        else:

            state = nafshi_to_genral_region.get(str(document.location1), "")
            document_dict = {
                "title": document.serviceName,
                "description": description,
                "phone_number": document.phoneNumber,
                "source": SourceType.NAFSHI.name,
                "website": document.serviceLink,
                "state": state,
                "audience": audiences
            }
            
            documents_final.append(Document(**document_dict))

        return documents_final


if __name__ == '__main__':
    nafshi_feed = NafshiFeed()

    records = nafshi_feed.pull()
