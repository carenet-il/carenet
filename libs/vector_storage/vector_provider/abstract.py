import hashlib
from abc import ABC, abstractmethod
from typing import List
from typing import Optional

from libs.embedding.abstract import EmbeddingAbstract
from libs.interfaces.document import Document, DocumentSearchFilters

class VectorProviderAbstract(ABC):
    def __init__(self, embedding_model: EmbeddingAbstract):
        self.embedding_model = embedding_model

    @abstractmethod
    def insert_many(self, documents: List[Document]):
        pass

    @abstractmethod
    def delete_all(self):
        pass

    @abstractmethod
    def search(
            self, query: str, filters: Optional[DocumentSearchFilters] = None
    ) -> List[Document]:
        pass

    def generate_id(self, doc: Document) -> str:
        return hashlib.md5(
            doc.title.encode("utf-8") + doc.source.encode("utf-8")
        ).hexdigest()
        
    @abstractmethod
    def fetch_search_filters(self) -> DocumentSearchFilters:
        """
        Will return the search filters that are available for the current vector provider,
        and the values that are available for each filter.
        """
        pass