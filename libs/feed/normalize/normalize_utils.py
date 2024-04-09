import textdistance

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

def normalize_treatments(supplier: dict) -> str:
    treatments = []

    services = [{
        "ServiceDescription": service.get("ServiceDescription", ""),
        "Treatments": [treatment.get("TreatmentDescription", "") for treatment in
                       service.get("Treatments", [])]
    } for service in supplier.get("Services", [])]

    for service in services:
        for treat in service["Treatments"]:
            if treat not in treatments:
                treatments.append(treat)

    return ', '.join(treatments)


def normalize_telephones(supplier: dict) -> str:
    ans = []
    telephones = [supplier.get("TelephoneA", ""),
                  supplier.get("TelephoneB", ""),
                  supplier.get("TelephoneC", ""),
                  supplier.get("TelephoneD", "")]

    for tel in telephones:
        if tel == '' or tel is None:
            continue
        ans.append(tel)

    return ','.join(ans)