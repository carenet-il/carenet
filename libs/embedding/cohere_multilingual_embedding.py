import os
from abc import ABC
from typing import List
from libs.embedding.abstract import EmbeddingAbstract
import cohere

from libs.utils.cache import lru_cache_with_ttl


class CohereMultilingualEmbedding(EmbeddingAbstract, ABC):
    def __init__(self, load_locally_model=True):
        self.load_locally_model = load_locally_model
        self.co = cohere.Client(os.getenv("COHERE_API"))  # This is your trial API key

    def encode_bulk(self, texts: List[str]) -> List[List[float]]:
        return self.request_to_model_api(texts)

    def encode(self, text: str) -> List[float]:
        results = self.request_to_model_api([text])
        if len(results) > 0:
            return results[0]

        return []

    @lru_cache_with_ttl(maxsize=None, ttl=120)
    def request_to_model_api(self, texts: List[str]) -> List[List[float]]:

        try:
            response = self.co.embed(
                model='embed-multilingual-light-v3.0',
                texts=texts,
                input_type='classification'
            )
            return response.embeddings
        except Exception as error:
            print(error)
            return []
