import re
import requests
from libs.interfaces.document import Document
import textdistance
from .cities import cities_israel_heb


def get_locations_by_coordination(lat: float, lon: float):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Depending on the response structure, you might need to adjust the keys
        full_location = data.get("display_name", "")
        address = data.get("address", {})
        city = address.get("city", address.get("town", address.get("village", "")))
        state = address.get("state", "")
        return full_location, city, state
    else:
        return "", "", ""


def extract_phone(text: str):
    if not text:
        return ""

    # Regular expression for extracting phone numbers
    phone_pattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
    matches = phone_pattern.findall(text)

    return ', '.join(matches) if matches else ""


def extract_email(text: str):
    if not text:
        return ""

    # Regular expression for extracting email addresses
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    match = email_pattern.search(text)

    return match.group() if match else ""


def extract_description(text):
    if not text:
        return ""

    # Regular expression to identify HTML tags
    tag_re = re.compile(r'<[^>]+>')

    # Remove the HTML tags
    return tag_re.sub('', text)

def extract_labeled_region_from_text(text: str) -> str:
    """Extracts the region from a given string"""

    # regular expression to match 'מחוז' followed by any characters except ',' (non-greedy) until a ','
    pattern = r"מחוז(.*?),"
    
    regions = ['מחוז ירושלים','מחוז הצפון','מחוז הדרום','מחוז חיפה','מחוז תל אביב','ארצי - מרחוק','מחוז המרכז']

    # search for the pattern in the text
    match = re.search(pattern, text)

    region = "מחוז " + match.group(1).strip() if match else ''
    
    return region if region in regions else ''


def extract_region_by_city(city: str) -> str:
    """This function gets a city and return its region using the api of openstreetmap """

    try:
        url = f'https://nominatim.openstreetmap.org/search?city={city}&format=json&accept-language=he'
        response = requests.get(url).json()[0]  # take the first record, sometimes it returns more than one

        city_details = response.get('display_name', "")  # example of the var : עכו, נפת עכו, מחוז הצפון, ישראל

        # happens when there is no such city in the API or city name is not in the api dataset
        
        return '' if len(city_details) == 0 else extract_labeled_region_from_text(city_details)

    except Exception as e:
        return ''
    

def join_elements_with_separator(elements: list) -> str:
    if len(elements) == 0:
        return ''
    else:
        concatenated_string = ', '.join(elements)
        return concatenated_string
    

def extract_geo_loc_from_city(city: str) -> tuple:
    """Query the OpenStreetMap Nominatim API to get latitude and longitude for a given city """
    if city == '':
        return 91,-91
    try:
        url = f'https://nominatim.openstreetmap.org/search?city={city}&format=json&limit=1'
        
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json()
            if results:
                # extract latitude and longitude from the first result
                latitude = results[0].get('lat')
                longitude = results[0].get('lon')
                return float(latitude), float(longitude)
            else:
                return 91,-91
        else:
            return 91,-91
    except Exception as e:
        print(f"Error fetching geolocation for city '{city}': {e}")
        return 91,-91


def insert_geo_loc_to_doc(docs:list[Document]) -> list[Document]:
        
    for doc in docs:
        city = doc.city if doc.city else ''  # Using dot notation to access attributes
        latitude, longitude = extract_geo_loc_from_city(city)
        
        # updating the document's attribute's
        doc.latitude = latitude
        doc.longitude = longitude
                
    return docs

def extract_geo_loc_from_region(region:str):        
    """Query the OpenStreetMap Nominatim API to get latitude and longitude for a given region """\
        
    if region == 'ארצי - מרחוק':
        return 91,-91
    
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={region}"
        
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json()
            if results:
                # extract latitude and longitude from the first result
                latitude = results[0].get('lat')
                longitude = results[0].get('lon')
                return str(latitude), str(longitude)
            else:
                return 91,-91
        else:
            return 91,-91
    except Exception as e:
        print(f"Error fetching geolocation for city '{region}': {e}")
        return 91,-91
    
def find_best_city_match_israel(docs:list[Document]) -> Document:
    '''This function loop all the city & Regional Council in israel and find the best match using Jaro-Winkler similarity score'''
    
    for doc in docs:
        highest_score = 0
        best_match = ""
        for actual_city in cities_israel_heb:
            score = textdistance.jaro_winkler(doc.city, actual_city)
            if score > highest_score:
                highest_score = score
                best_match = actual_city
                
        doc.city = best_match
    
    return docs