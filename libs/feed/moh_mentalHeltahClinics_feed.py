from abc import ABC
import requests
from libs.feed.abstract import FeedAbstract

from libs.interfaces.document import Document, SourceType
from libs.feed.extractors.extractors import extract_region_from_city

class MOH_MentalHealthClinicsFeed(FeedAbstract, ABC):

    def pull(self) -> list[Document]:
        
        documents: list[Document] = []
                
        url = 'https://data.gov.il/api/3/action/datastore_search?resource_id=f7a7b061-db5b-4e19-b1bf-2d7525af52ca&'

        response:list = requests.post(url).json().get('result').get('records')
                        
        for doc in response:
            documents.append(self.__norm_document__(doc))
            
        print(f'Found at ministry of health mental health clinics {len(documents)} documents')
                
        return documents

    def __norm_document__(self,document) -> Document:
        
        clinic_code_to_str = {
            
            "1":'למבוטחי קופת חולים בלאומית',
            "2":'למבוטחי קופת חולים מכבי',
            "3":'למבוטחי קופת חולים כללית',
            "4":'למבוטחים קופת חולים לאומית',
            "5":'למבוטחי כל הקופות',
            
        }
        
        intervention_type = document.get('intervention_type','')
        if intervention_type == 'אין נתונים':
            intervention_type = ''
        
        specialization = document.get('specialization','')
        if specialization == 'אין נתונים':
            specialization = ''
            
        
        phone_number = document.get('אין נתונים','')
        if phone_number == 'אין נתונים':
            phone_number = ''
    
        # extract the name of the helath care company using the HMO_code
        health_care_company = clinic_code_to_str.get(document.get("HMO_code",""), "")
        
        document_dict = {
            "title": f'{document.get("clinic_name","")} {document.get("audience","")} {health_care_company}',
            "description": f'{intervention_type} {specialization}',
            "phone_number": phone_number,
            "source": SourceType.MOH.name,
            "full_location": document.get('street', ''),
            "city": document.get('city',''),
            "state": extract_region_from_city(document.get('city','')),
        }

        return Document(**document_dict)



