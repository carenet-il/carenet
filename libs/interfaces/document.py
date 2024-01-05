from enum import Enum
from typing import List

from pydantic import BaseModel, EmailStr, constr


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
    id: str
    name: str
    title: str
    description: str
    age: AgeTag
    email: EmailStr
    phone_number: constr(regex=r'^\+\d{1,3}-\d{1,10}$')  # Simple regex for phone numbers
    source: SourceType
    location: Location


class EmbeddingDocumentMetaData(BaseModel):
    original_document: Document
    name: str
    title: str
    description: str
    age: AgeTag
    email: EmailStr
    phone_number: constr(regex=r'^\+\d{1,3}-\d{1,10}$')  # Simple regex for phone numbers
    source: SourceType
    location: Location


class EmbeddingDocument(BaseModel):
    id: str
    values: List[float]
    metadata: EmbeddingDocumentMetaData

    @property
    def id(self):
        return self.id
