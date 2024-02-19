from fastapi import APIRouter, HTTPException
from libs.interfaces.document import Document
from libs.vector_storage.vector_provider.extract_radius import extract_docs_from_radius
from services import vector_storage
from .models import SearchDocumentResult, SearchDocumentPayload
from libs.vector_storage.vector_provider.mongodb import MongoVectorProvider

router = APIRouter()


@router.post("/search", response_model=SearchDocumentResult)
def search(payload: SearchDocumentPayload):
    res = vector_storage.search(query=payload.query, filters=payload.filters, threshold=payload.threshold)

    return {"results": res}


# @router.post("/")
def upload_documents():
    return {"message": "Hello World"}


@router.get("/extract-from-radius", response_model=SearchDocumentResult)
def docs_from_radius(city_name: str, radius: str):
    """
    Extract documents within a specified radius of a city.
    
    - city_name: name of the city to search around
    - radius: radius in kilometers around the city to search within
    """
    try:
        
        document_collection = MongoVectorProvider.get_document_collection()
        results:list[Document] = extract_docs_from_radius(document_collection, city_name, radius)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return results

