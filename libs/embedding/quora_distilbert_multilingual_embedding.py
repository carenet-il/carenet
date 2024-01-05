from abc import ABC
from typing import List

from sentence_transformers import SentenceTransformer

from libs.embedding.abstract.embedding_abstract import EmbeddingAbstract


class QuoraDistilBertMultilingualEmbedding(EmbeddingAbstract, ABC):

    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/quora-distilbert-multilingual')

    def encode(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()
