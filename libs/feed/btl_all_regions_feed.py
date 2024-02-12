from abc import ABC
from bs4 import BeautifulSoup
import requests
from libs.feed.abstract import FeedAbstract
from libs.feed.extractors.extractors import extract_region_by_city
import pandas as pd
import json

from libs.interfaces.document import Document, SourceType

url_north = 'https://www.btl.gov.il/HaravotBarzel1/Harada_HB/Pages/MercazeiHOSEN_zafon_hb.aspx'
url_south = 'https://www.btl.gov.il/HaravotBarzel1/Harada_HB/Pages/MercazeiOsenDaromHB.aspx'
url_central_sharon = 'https://www.btl.gov.il/HaravotBarzel1/Harada_HB/Pages/HOZENmercazhb.aspx'
url_jerusalem_samaria = 'https://www.btl.gov.il/HaravotBarzel1/Harada_HB/Pages/YerushalaimYoshHB.aspx'

# URLs with corresponding region names
region_urls = [url_north,url_south,url_central_sharon,url_jerusalem_samaria]

def clean_text(text):
    # remove zero width space characters
    return text.replace('\u200b', '').strip()

class BtlFeed(FeedAbstract, ABC):
    
    def pull(self) -> list[Document]:
        
        documents:list[Document] = []

        for url in region_urls:

            response = requests.get(url)
            html_content = response.content

            # parse the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')
            table = soup.find('table', {'class': 'btl-rteTable-default'})

            # convert table to DataFrame
            rows = []
            for tr in table.find_all('tr'):
                cells = tr.find_all(['th', 'td'])
                row = [clean_text(cell.text) for cell in cells]  # Apply clean_text to each cell's text
                rows.append(row)

            df = pd.DataFrame(rows[1:], columns=rows[0])            

            # from data-frame to string
            json_string = df.to_json(orient='records', force_ascii=False)

            # from string to json
            json_data = json.loads(json_string)

            for record in json_data:

                # edge-case for 'מגידו' that don't have a phone number
                if record.get('ישוב') == 'מגידו':
                    continue

                # edge-case because miss info from the website
                if record.get('טלפון') == '​צור משה, נתניה':
                    record['טלפון'] = record.get('כתובת',"") # switch between them
                    record['כתובת'] = 'הצורן 2, נתניה' # the address not appear on the web       
                
                # checks if the url is for jerusalem and samaria, and use the "מחוז ירושלים" as a region
                if url == url_jerusalem_samaria:
                    record['state'] = "מחוז ירושלים"
                    
                else: # if not, use the function extract_region_by_city
                    record['state'] = extract_region_by_city(record['ישוב']) # the function returns an empty string if not found

                # norm the record
                norm_doc = self.__norm_document__(record)
                documents.append(norm_doc)
                
        print(f'Found at BTL all regions {len(documents)} documents')
    
        return documents

    def __norm_document__(self, document) -> Document:
        
        document_dict = {
            "title": f' מרכז חוסן {document.get("מרפאה", "")}',
            "description": "",
            "phone_number": document.get("טלפון", ""),
            "source": SourceType.BTL.name,  # BTL stands for 'ביטוח לאומי'
            "full_location": document.get("כתובת", ""),
            "city": document.get("ישוב", ""),
            "state" : document.get("state", "")
        }

        return Document(**document_dict)