from pydantic import BaseModel

class SearchDocumentResult(BaseModel):
    results: list
