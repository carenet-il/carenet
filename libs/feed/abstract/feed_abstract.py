from abc import ABC, abstractmethod
from typing import List

import requests

from libs.interfaces.document import Document


def get_location(lat: float, lon: float):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    response = requests.get(url)
    data = response.json()
    return data.get("display_name")


class FeedAbstract(ABC):

    @abstractmethod
    def pull(self) -> List[Document]:
        pass

    @abstractmethod
    def __norm_document__(self, document) -> Document:
        pass
