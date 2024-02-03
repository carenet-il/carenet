from pydantic import BaseModel, Field
from libs.interfaces.document import DocumentSearchFilters


class GetFiltersResult(BaseModel):
    results: DocumentSearchFilters = Field(...)
