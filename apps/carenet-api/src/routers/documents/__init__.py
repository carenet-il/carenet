from fastapi import APIRouter, Depends
from .models import SearchDocumentQuery

router = APIRouter()

@router.get("/search")
async def search(
    query: SearchDocumentQuery = Depends(),
):
    return {"message": "Hello World", "query": query}


@router.post("/")
async def upload_documents():
    return {"message": "Hello World"}
