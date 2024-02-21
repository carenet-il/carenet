from fastapi import APIRouter, HTTPException
from services import vector_storage
from .models import SearchDocumentResult, SearchDocumentPayload

router = APIRouter()


@router.post("/search", response_model=SearchDocumentResult)
def search(payload: SearchDocumentPayload):
    res = vector_storage.search(query=payload.query, filters=payload.filters, threshold=payload.threshold)

    return {"results": res}


# @router.post("/")
def upload_documents():
    return {"message": "Hello World"}

