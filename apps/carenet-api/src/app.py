from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import documents

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://carenet-il.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/documents", tags=["documents"])
