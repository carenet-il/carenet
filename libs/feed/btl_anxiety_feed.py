from abc import ABC
from bs4 import BeautifulSoup
import requests
from libs.feed.abstract import FeedAbstract
import pandas as pd
import json

from libs.interfaces.document import Document, SourceType
from libs.feed.btl_all_regions_feed import clean_text
from libs.feed.extractors.extractors import extract_region_by_city

class BtlAnxietyFeed(FeedAbstract, ABC):

    def pull(self) -> list[Document]:
        documents: list = []

        url = 'https://www.btl.gov.il/benefits/Victims_of_Hostilities/Pages/%D7%9E%D7%A8%D7%9B%D7%96.aspx'
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

            # edge case for one record that return 5 values instead of 4 like it should be as the number of columns
            if len(row) == 5:
                rows.append(row[:-1])
            else:
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

            # edge-case because in the html content this record is inside a table that is inside a table
            # I added a pic of the html content in this link: https://drive.google.com/file/d/1w2D9Q5fZsEEhcB4ABBNtuGMxUSwOEjSz/view?usp=sharing
            if record.get('ישוב') == 'משגב - כרמיאל':
                record['מרפאה'] = 'משגב - כרמיאל'
                record['טלפון'] = '04-9922091 שלוחה 1 או 2'
                record['כתובת'] = 'הגפן 13, כרמיאל'
                
            # for all regions to be the same, we use open map street api
            record['state'] = extract_region_by_city(record['ישוב']) # the function returns an empty string if not found

            # norm the record
            norm_doc = self.__norm_document__(record)
            documents.append(norm_doc)

        print(f'Found at BTL anxiety {len(documents)} documents')

        return documents

    def __norm_document__(self,document) -> Document:
        document_dict = {
            "title": f' מרכז חוסן {document.get("מרפאה", "")}',
            "description": "",
            "phone_number": document.get("טלפון", ""),
            "source": SourceType.BTL.name,
            "full_location": document.get("כתובת", ""),
            "city": document.get("ישוב", ""),
            "state": document.get("state", "")
        }

        return Document(**document_dict)



