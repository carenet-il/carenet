from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field, conlist


class SourceType(Enum):
    N12 = "N12"
    # Add other source types as needed


class Document(BaseModel):
    title: str
    description: str
    email: Optional[str] = Field(default="")
    phone_number: Optional[str] = Field(default="")
    source: str
    full_location: str
    city: Optional[str] = Field(default="")
    state: Optional[str] = Field(default="")
    score: Optional[float] = Field(default=0)


class EmbeddingDocument(BaseModel):
    id: str
    values: list[float]
    metadata: Document


class DocumentSearchFilters(BaseModel):
    city: Optional[Union[str, conlist(str, min_length=1, unique_items=True)]] = Field(
        default=None
    )
    state: Optional[Union[str, conlist(str, min_length=1, unique_items=True)]] = Field(
        default=None
    )
