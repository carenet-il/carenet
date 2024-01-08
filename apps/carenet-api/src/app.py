from fastapi import FastAPI
from routers import documents

app = FastAPI()


app.include_router(documents.router, prefix="/documents", tags=["documents"])
