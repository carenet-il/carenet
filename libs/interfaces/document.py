from pydantic import BaseModel, EmailStr, constr
from enum import Enum
from typing import List, Optional


class AgeTag(Enum):
    CHILD = 'child'
    TEEN = 'teen'
    ADULT = 'adult'
    SENIOR = 'senior'


class SourceType(Enum):
    N12 = 'N12'
    # Add other source types as needed


class Location(Enum):
    LOCATION1 = 'Location1'
    LOCATION2 = 'Location2'
    # Add other locations as needed


class Document(BaseModel):
    name: str
    title: str
    description: str
    age: AgeTag
    email: EmailStr
    phone_number: constr(regex=r'^\+\d{1,3}-\d{1,10}$')  # Simple regex for phone numbers
    source: SourceType
    location: Location
