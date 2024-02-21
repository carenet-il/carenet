import requests

from libs.interfaces.document import Document, LocationGeo
from libs.utils.cache import lru_cache_with_ttl



@lru_cache_with_ttl(maxsize=None, ttl=120)
def get_cities_israel_heb() -> list[str]:
    url = "https://data.gov.il/api/3/action/datastore_search?resource_id=5c78e9fa-c2e2-4771-93ff-7f400a12f7ba&limit=2000"

    response = requests.request("GET", url)

    response = response.json()

    # remove spaces
    cities = list(map(lambda x: str(x["שם_ישוב"]).strip(), response["result"]["records"]))

    return cities

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


def insert_location_object_to_documents_by_city_or_state(docs: list[Document]) -> list[Document]:
    for doc in docs:
        if doc.city != '':
            latitude, longitude = extract_geo_loc_from_city(doc.city)

            if latitude is not None and longitude is not None:
                doc.location = LocationGeo(**{
                    "type": "Point",
                    "coordinates": [longitude, latitude]  # longitude, latitude
                })
        elif doc.state != '':
            latitude, longitude = extract_geo_loc_from_region(doc.state)

            if latitude is not None and longitude is not None:
                doc.location = LocationGeo(**{
                    "type": "Point",
                    "coordinates": [longitude, latitude]  # longitude, latitude
                })

    return docs
