from enum import Enum
from typing import Optional, Union, Dict, Tuple, List

from pydantic import BaseModel, Field, conlist


class SourceType(Enum):
    N12 = "N12"
    NAFSHI = "NAFSHI"
    MOH = "Ministry of Health"
    BTL = "BTL"
    OTEFLEV = "OTEFLEV"
    # Add other source types as needed


class LocationGeo(BaseModel):
    type: str = Field(default="Point")
    coordinates: Tuple[float, float] = Field(..., description="A tuple of two floats representing longitude and latitude")


class Document(BaseModel):
    title: str
    description: str
    source: str
    email: Optional[str] = Field(default="")
    website: Optional[str] = Field(default="")
    phone_number: Optional[str] = Field(default="")
    full_location: Optional[str] = Field(default="")
    city: Optional[str] = Field(default="")
    audience: Optional[List[str]] = Field(default=[])
    state: Optional[str] = Field(default="")
    score: Optional[float] = Field(default=0)
    id: Optional[str] = Field(default="")
    location: Optional[LocationGeo] = Field(default=None)
    '''
    Example of location value:
        
    location = {
        "type": "Point",
        "coordinates": [-73.856077, 40.848447]  # longitude, latitude
    }
    '''

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
        location = "location"
        state = "state"
        score = "score"
        audience = "audience"
        id = "id"


class EmbeddingDocument(BaseModel):
    id: str
    values: list[float]
    metadata: Document


class DocumentSearchFilters(BaseModel):
    """
    Defines the filters that can be applied when searching for documents.
    """

    city: Optional[Union[str, conlist(str, min_length=1)]] = Field(
        default=None,
        description="The city or cities to filter the documents by. Can be a single city or a list of cities."
    )
    radius: Optional[int] = Field(
        default=None,
        description="The radius in meters to search around the specified city or cities. Only applies when a city is specified."
    )
    state: Optional[Union[str, conlist(str, min_length=1)]] = Field(
        default=None,
        description="The state or states to filter the documents by. Can be a single state or a list of states."
    )
    audience: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="The target audience or audiences for the documents. Can be a single audience category or a list of categories."
    )
