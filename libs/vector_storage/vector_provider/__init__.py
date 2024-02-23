

from libs.embedding.abstract import EmbeddingAbstract
from libs.vector_storage.vector_provider.mongodb import MongoVectorProvider
import os


if __name__ == "__main__":
    
    # for testing    
    provider = MongoVectorProvider(embedding_model=EmbeddingAbstract, db_name='dev',mongodb_uri=os.getenv("MONGO_URI"))
    provider.delete_all()
    

