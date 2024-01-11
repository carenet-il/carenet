import re
from abc import ABC, abstractmethod
from typing import List

import requests

from libs.interfaces.document import Document


def get_locations_by_coordination(lat: float, lon: float):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Depending on the response structure, you might need to adjust the keys
        full_location = data.get("display_name")
        address = data.get("address")
        city = address.get("city", address.get("town", address.get("village", "")))
        state = address.get("state", "")
        return full_location, city, state
    else:
        return "", "", ""


def extract_phone(phone: str):
    if not phone:
        return ""

    # Regular expression for extracting phone numbers
    phone_pattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
    matches = phone_pattern.findall(phone)

    return ', '.join(matches) if matches else ""


def extract_email(email: str):
    if not email:
        return ""

    # Regular expression for extracting email addresses
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    match = email_pattern.search(email)

    return match.group() if match else ""


def extract_description(description):
    if not description:
        return ""

    # Regular expression to identify HTML tags
    tag_re = re.compile(r'<[^>]+>')

    # Remove the HTML tags
    return tag_re.sub('', description)


class FeedAbstract(ABC):

    @abstractmethod
    def pull(self) -> List[Document]:
        pass

    @abstractmethod
    def __norm_document__(self, document) -> Document:
        pass
