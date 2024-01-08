from pydantic import BaseModel
from fastapi import Query
from libs.interfaces.document import AgeTag, SourceType
from typing import Optional

class SearchDocumentQuery(BaseModel):
    query: Optional[str] = Query(None, description="Query string to search for")
    age: Optional[AgeTag] = Query(None, description="Age tag to filter by")
