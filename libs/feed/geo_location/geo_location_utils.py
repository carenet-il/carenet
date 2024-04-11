import json
from typing import List

import requests
from tqdm import tqdm

from libs.feed.extractors.extractors import extract_center_city_from_state
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from libs.interfaces.document import Document, LocationGeo
from libs.utils.cache import lru_cache_with_ttl



@lru_cache_with_ttl(maxsize=None, ttl=120)
def get_cities_israel_heb() -> list[str]:
    try:
        # Correctly load the local JSON file as a fallback
        with open('libs/feed/geo_location/israel_cities.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except Exception as e:  # It's better to catch specific exceptions, this is just an example
        print(f"Failed to load fallback JSON: {e}")
        return []

    # remove spaces
    cities = list(map(lambda x: str(x["שם_ישוב"]).strip(), data["result"]["records"]))

    return sorted(cities)

@lru_cache_with_ttl(maxsize=None, ttl=120)
def extract_geo_loc_from_city(city: str) -> tuple:
    """Query the OpenStreetMap Nominatim API to get latitude and longitude for a given city """
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
                return None, None
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching geolocation for city '{city}': {e}")
        return None, None

# todo: not been used in this project. can be removed.
@lru_cache_with_ttl(maxsize=None, ttl=120)
def extract_geo_loc_from_region(region: str):
    """Query the OpenStreetMap Nominatim API to get latitude and longitude for a given region """
    if region == 'ארצי - מרחוק':
        return None, None

    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={region}"

        response = requests.get(url)
        if response.status_code == 200:
            results = response.json()
            if results:
                # extract latitude and longitude from the first result
                latitude = results[0].get('lat')
                longitude = results[0].get('lon')
                return float(latitude), float(longitude)
            else:
                return None, None
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching geolocation for city '{region}': {e}")
        return None, None




def process_document_insert_location(doc:Document):
    """
    Process a single document to add location information based on city or state.
    """
    if doc.city:
        latitude, longitude = extract_geo_loc_from_city(doc.city)

        if latitude is not None and longitude is not None:
            doc.location = LocationGeo(**{
                "type": "Point",
                "coordinates": [longitude, latitude]  # longitude, latitude
            })
    elif doc.state:
        center_city_inside_state = extract_center_city_from_state(doc.state)

        latitude, longitude = extract_geo_loc_from_city(center_city_inside_state)

        if latitude is not None and longitude is not None:
            doc.location = LocationGeo(**{
                "type": "Point",
                "coordinates": [longitude, latitude]  # longitude, latitude
            })

    return doc


def insert_location_object_to_documents_by_city_or_state(docs: List[Document]):
    """
    Modify the documents list to include location objects for documents based on city or state, using 20 threads.
    """
    # Use ThreadPoolExecutor to parallelize the operation
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit all documents to the executor
        future_to_doc = {executor.submit(process_document_insert_location, doc): doc for doc in docs}

        # Use tqdm to show progress
        for future in tqdm(as_completed(future_to_doc), total=len(docs)):
            try:
                # This will also raise any exceptions caught during the execution of the task.
                future.result()
            except Exception as exc:
                print(f"Generated an exception: {exc}")

    return docs
