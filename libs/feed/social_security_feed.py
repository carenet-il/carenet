from abc import ABC
from bs4 import BeautifulSoup
import requests
from libs.feed.abstract import FeedAbstract
import pandas as pd
import json

from libs.interfaces.document import Document, SourceType

url_north = 'https://www.btl.gov.il/HaravotBarzel1/Harada_HB/Pages/MercazeiHOSEN_zafon_hb.aspx'
url_south = 'https://www.btl.gov.il/HaravotBarzel1/Harada_HB/Pages/MercazeiOsenDaromHB.aspx'
url_central_Sharon = 'https://www.btl.gov.il/HaravotBarzel1/Harada_HB/Pages/HOZENmercazhb.aspx'
url_Jerusalem_Samaria = 'https://www.btl.gov.il/HaravotBarzel1/Harada_HB/Pages/YerushalaimYoshHB.aspx'

# URLs with corresponding region names
region_urls = {
    url_north: 'Northern',
    url_south: 'Southern',
    url_central_Sharon: 'Central Sharon',
    url_Jerusalem_Samaria: 'Jerusalem Samaria'
}

class SocSecFeed(FeedAbstract, ABC):


    def clean_text(self,text):
        # remove zero width space characters
        return text.replace('\u200b', '').strip()
    
    def pull(self) -> list[Document]:
        
        documents:list[Document] = []

        for url, region in region_urls.items():

            response = requests.get(url)
            html_content = response.content

            # parse the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')
            table = soup.find('table', {'class': 'btl-rteTable-default'})

            # convert table to DataFrame
            rows = []
            for tr in table.find_all('tr'):
                cells = tr.find_all(['th', 'td'])
                row = [self.clean_text(cell.text) for cell in cells]  # Apply clean_text to each cell's text
                rows.append(row)

            print(f'The number of documents from the {region} region is: {len(rows) - 1}')

            df = pd.DataFrame(rows[1:], columns=rows[0])

            # from data-frame to string
            json_string = df.to_json(orient='records', force_ascii=False)

            # from string to json
            json_data = json.loads(json_string)

            for record in json_data:
                norm_doc = self.__norm_document__(record)
                documents.append(norm_doc)
        
        print(f'number of documents from social security - {len(documents)}')

        return documents

    def __norm_document__(self, document) -> Document:

        document_dict = {
            "title": f' מרכז חוסן {document.get("מרפאה", "")}',
            "description": "",
            "phone_number": document.get("טלפון", ""),
            "source": SourceType.SOCSEC.name,  # SOCSEC stands for Social Security
            "full_location": document.get("כתובת", ""),
            "city": document.get("ישוב'", ""),
        }

        return Document(**document_dict)