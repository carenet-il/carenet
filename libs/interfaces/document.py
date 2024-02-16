from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field, conlist


class SourceType(Enum):
    N12 = "N12"
    NAFSHI = "NAFSHI"
    MOH = "Ministry of Health"
    BTL = "BTL"
    OTEFLEV = "OTEFLEV"
    # Add other source types as needed

class Document(BaseModel):
    title: str
    description: str
    source: str
    email: Optional[str] = Field(default="")
    website: Optional[str] = Field(default="")
    phone_number: Optional[str] = Field(default="")
    full_location: Optional[str] = Field(default="")
    city: Optional[str] = Field(default="")
    latitude: Optional[float] = Field(default= -91)
    longitude: Optional[float]= Field(default= 91)
    state: Optional[str] = Field(default="")
    score: Optional[float] = Field(default=0)

    class Fields:
        """
        To prevent hardcoding field names in the code, we can use this class to store the field names.
        """
        title = "title"
        description = "description"
        source = "source"
        email = "email"
        website = "website"
        phone_number = "phone_number"
        full_location = "full_location"
        city = "city"
        state = "state"
        score = "score"
        latitude = "latitude"
        longitude = "longitude"
        

class EmbeddingDocument(BaseModel):
    id: str
    values: list[float]
    metadata: Document


class DocumentSearchFilters(BaseModel):
    city: Optional[Union[str, conlist(str, min_length=1)]] = Field(
        default=None
    )
    state: Optional[Union[str, conlist(str, min_length=1)]] = Field(
        default=None
    )
