from fastapi import APIRouter, HTTPException
from services import vector_storage
from .models import GetFiltersResult

router = APIRouter()


@router.get("/", response_model=GetFiltersResult)
def search():
    try:
        res = vector_storage.fetch_search_filters()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"results": res}

