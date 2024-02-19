from libs.interfaces.document import Document
from libs.feed.extractors.extractors import extract_point_from_city


def extract_docs_from_radius(document_collection, city_name: str, radius: str) -> list[Document]:

    point = extract_point_from_city(city_name)

    # normalize the radius
    radius = int(radius) * 1000  # Adjusted to multiply by 1000 for meters

    query = [
        {
            '$geoNear': {
                'near': point,
                'distanceField': "dist.calculated",
                'maxDistance': radius,
                'query': {'type': "public"},
                'includeLocs': "dist.location",
                'spherical': True
            }
        }
    ]

    results = document_collection.aggregate(query)

    return [Document(**doc) for doc in results]
