from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class AgeTag(Enum):
    CHILD = 'child'
    TEEN = 'teen'
    ADULT = 'adult'
    SENIOR = 'senior'


class SourceType(Enum):
    N12 = 'N12'
    # Add other source types as needed


class Document(BaseModel):
    id: Optional[str]
    title: str
    description: str
    age: Optional[AgeTag]
    email: str
    phone_number: Optional[str]
    source: SourceType
    location: str


class EmbeddingDocumentMetaData(BaseModel):
    original_document: Document
    name: str
    title: str
    description: str
    age: Optional[AgeTag]
    email: str
    phone_number: Optional[str]
    source: SourceType
    location: str


class EmbeddingDocument(BaseModel):
    id: str
    values: List[float]
    metadata: EmbeddingDocumentMetaData

    @property
    def id(self):
        return self.id
