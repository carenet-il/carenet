import textdistance
from libs.feed.extractors.extractors import extract_city_from_region

from libs.interfaces.document import Document
from libs.utils.cache import lru_cache_with_ttl


@lru_cache_with_ttl(maxsize=None, ttl=120)
def find_best_city_match(cities_israel_heb: tuple[str], city: str):
    highest_score = 0
    best_match = ""
    for actual_city in cities_israel_heb:
        score = textdistance.jaro_winkler(city, actual_city)
        if score > highest_score:
            highest_score = score
            best_match = actual_city

    return best_match


def normalize_cities(cities_israel_heb: list[str], docs: list[Document]) -> list[Document]:
    """This function loop all the city & Regional Council in israel and find the best match using Jaro-Winkler
    similarity score"""
    for doc in docs:
        if doc.city:
            doc.city = find_best_city_match(tuple(cities_israel_heb), doc.city)

    return docs
