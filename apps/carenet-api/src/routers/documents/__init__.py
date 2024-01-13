from fastapi import APIRouter, Query
from services import vector_storage
from typing import Optional, Union
from .models import SearchDocumentResult

router = APIRouter()


@router.get("/search", response_model=SearchDocumentResult)
async def search(
    search: str = Query(..., description="Query string to search for"),
    city: Optional[Union[str, list[str]]] = Query(
        None, description="City to search in"
    ),
):
    res = vector_storage.search(query=search, filters={})

    return {"results": res}


@router.post("/")
async def upload_documents():
    return {"message": "Hello World"}
