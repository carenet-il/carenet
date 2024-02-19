import requests

from libs.interfaces.document import Document, LocationGeo


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


def insert_geo_loc_to_doc(docs: list[Document]) -> list[Document]:
    for doc in docs:
        if doc.city != '':
            latitude, longitude = extract_geo_loc_from_city(doc.city)

            if latitude is not None and longitude is not None:
                doc.location = LocationGeo(**{
                    "type": "Point",
                    "coordinates": [longitude, latitude]  # longitude, latitude
                })
        elif doc.state:
            latitude, longitude = extract_geo_loc_from_region(doc.state)

            if latitude is not None and longitude is not None:
                doc.location = LocationGeo(**{
                    "type": "Point",
                    "coordinates": [longitude, latitude]  # longitude, latitude
                })

    return docs




def extract_point_from_city(city_name: str) -> dict:
    latitude, longitude = extract_geo_loc_from_city(city_name)

    location = {
        "type": "Point",
        "coordinates": [longitude, latitude]  # longitude, latitude
    }

    return location
