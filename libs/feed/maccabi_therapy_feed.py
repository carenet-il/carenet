from abc import ABC
import requests
from libs.feed.abstract import FeedAbstract
from bs4 import BeautifulSoup
import pandas as pd


from libs.feed.extractors.extractors import extract_and_add_email_to_docs, extract_rows_from_table
from libs.interfaces.document import Document, SourceType

class MaccabiTherapyClinicsFeed(FeedAbstract, ABC):

    def pull(self) -> list[Document]:
        
        documents: list[Document] = []
                        
        # The given URL
        url = 'https://www.maccabi4u.co.il/new/eligibilites/4767/'
        response = requests.get(url)
        html_content = response.content
        
        # parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        divided_box_containers = soup.find_all('div', {'class': 'divided-box-container'})

        # There is 25 containers, each container is a set of 5 regions, each 5 is a different kind of therapy
        # create a dict with the therapy kind as the key and the right container as the value
        treatment_container = {"הבעה ויצירה": divided_box_containers[:5],
                            "רכיבה טיפולית": divided_box_containers[5:10],
                            "תרפיה באמצעות בעלי חיים": divided_box_containers[10:15],
                            "ספורט טיפולי": divided_box_containers[15:20],
                            "פעילות טיפולית במים": divided_box_containers[20:25]}
        regions = [
            'מחוז הצפון',
            'מחוז המרכז',
            'מחוז תל אביב',
            'מחוז ירושלים',
            'מחוז הדרום'
        ]
        maccabi_url = 'https://www.maccabi4u.co.il/new/eligibilites/4767/'
        
        for treatment, containers in treatment_container.items():
            for container, region in zip(containers, regions):  # each container is a table
                table = container.find('div', {'class': 'd-table-desktop'})
                rows = extract_rows_from_table(table)

                df = pd.DataFrame(rows[1:], columns=rows[0])  # create a DataFrame from the rows

                # Add a new columns to the DataFrame. This automatically updates all rows.
                df['treat_type'] = treatment
                df['region'] = region
                df['website'] = maccabi_url

                # Convert the DataFrame to a list of dictionaries
                docs = df.to_dict(orient='records')
                extract_and_add_email_to_docs(docs)

                # Normalize the documents
                for new_doc in docs:
                    documents.append(self.__norm_document__(new_doc))
                                        
        print(f'Number of documents in Maccabi Therapy: {len(documents)}') 
             
        return documents

    def __norm_document__(self,document) -> Document:
        
        document_dict = {
            "title": document.get('treat_type', ''),
            "description": f"{document.get('מכון / מטפל', '')}, {document.get('treat_type', '')}",
            "phone_number": document.get('טלפון', ''),
            "source": SourceType.MACCABI_ART_THERAPY.name,
            "city": document.get('ישוב', ''),
            "full_location": f"{document.get('ישוב', '')}, {document.get('כתובת', '')}",
            "state": document.get('region', ''),
            "email": document.get('email', ''),
            "website": document.get('website', '')
        }

        return Document(**document_dict)




