from pydantic import BaseModel, Field
from libs.interfaces.document import Document, DocumentSearchFilters
from typing import Optional


class SearchDocumentPayload(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    filters: Optional[DocumentSearchFilters] = Field(default=None)
    # page: int = Field(..., ge=0)
    # limit: int = Field(..., ge=1, le=100)


class SearchDocumentResult(BaseModel):
    results: list[Document] = Field(...)
