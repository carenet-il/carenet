import re
import requests

from libs.utils.cache import lru_cache_with_ttl


@lru_cache_with_ttl(maxsize=None, ttl=120)
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


@lru_cache_with_ttl(maxsize=None, ttl=120)
def extract_phone(text: str):
    if not text:
        return ""

    # Regular expression for extracting phone numbers
    phone_pattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
    matches = phone_pattern.findall(text)

    return ', '.join(matches) if matches else ""


@lru_cache_with_ttl(maxsize=None, ttl=120)
def extract_email(text: str):
    if not text:
        return ""

    # Regular expression for extracting email addresses
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    match = email_pattern.search(text)

    return match.group() if match else ""


@lru_cache_with_ttl(maxsize=None, ttl=120)
def extract_description(text):
    if not text:
        return ""

    # Regular expression to identify HTML tags
    tag_re = re.compile(r'<[^>]+>')

    # Remove the HTML tags
    return tag_re.sub('', text)


@lru_cache_with_ttl(maxsize=None, ttl=120)
def extract_labeled_region_from_text(text: str) -> str:
    """Extracts the region from a given string"""

    # regular expression to match 'מחוז' followed by any characters except ',' (non-greedy) until a ','
    pattern = r"מחוז(.*?),"

    regions = ['מחוז ירושלים', 'מחוז הצפון', 'מחוז הדרום', 'מחוז חיפה', 'מחוז תל אביב', 'ארצי - מרחוק', 'מחוז המרכז']

    # search for the pattern in the text
    match = re.search(pattern, text)

    region = "מחוז " + match.group(1).strip() if match else ''

    return region if region in regions else ''


@lru_cache_with_ttl(maxsize=None, ttl=120)
def extract_region_from_city(city: str) -> str:
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


def extract_center_city_from_state(region: str) -> str:
    city_to_region = {
        "מחוז ירושלים": "ירושלים",
        "מחוז הצפון": "טבריה",
        "מחוז הדרום": "באר שבע",
        "מחוז חיפה": "חיפה",
        "מחוז תל אביב": "תל אביב - יפו",
        "מחוז המרכז": "ראשון לציון"
    }

    return city_to_region.get(region, "")


def extract_audience_from_doc(audience: str) -> str:
    # this function coverage all the optional audience in the feeds of Nafshi and Moh Mental Clinics and normalize them for filter operation
    if 'פעוטות וילדים' in audience:
        return 'ילדים ונוער'

    elif 'ילדים ונוער' in audience:
        return 'ילדים ונוער'

    elif 'בני נוער' in audience:
        return 'ילדים ונוער'

    elif 'צעירים' in audience:
        return 'מבוגרים'

    elif 'מבוגרים' in audience:
        return 'מבוגרים'

    elif 'אזרחים ותיקים' in audience:
        return 'מבוגרים'
    
    else:
        return ''
    
def extract_and_add_email_to_docs(docs):
    # Extract emails from phone_numbers values in maccabi feed and add them to the docs
    for doc in docs:
        phone_number_values = doc.get('טלפון', '').split(',')  # telephone value can include emails
        for element in phone_number_values:
            if '@' in element:  # means it's an email

                # adding the email to the doc
                doc['email'] = element

                # remove the email from the phone number value inside the doc
                phone_number_values.remove(element)

                # adding the phone number to the doc
                doc['טלפון'] = ','.join(phone_number_values)
                
def extract_rows_from_table(table):
    rows = []
    for tr in table.find_all('tr'):
        cells_data = []
        for cell in tr.find_all(['th', 'td']):
            # Extract all text parts within the cell; handles both single and multiple values
            parts = [part.strip() for part in cell.stripped_strings]
            cell_text = ','.join(parts)

            cells_data.append(cell_text)
        rows.append(cells_data)
    return rows