from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import documents, filters as filters_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://carenet-il.github.io",
    "https://carenet.free.nf",
    "https://carenet.co.il"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(filters_router.router, prefix="/filters", tags=["filters"])
