from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class SourceType(Enum):
    N12 = 'N12'
    # Add other source types as needed


class Document(BaseModel):
    title: str
    description: str
    email: Optional[str] = ''
    phone_number: Optional[str] = ''
    source: str
    full_location: str
    city: Optional[str] = ''
    state: Optional[str] = ''


class EmbeddingDocument(BaseModel):
    id: str
    values: List[float]
    metadata: Document
