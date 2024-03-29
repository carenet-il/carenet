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
        return self.request_to_model_api(tuple(texts))

    def encode(self, text: str) -> List[float]:
        results = self.request_to_model_api(tuple([text]))
        if len(results) > 0:
            return results[0]

        return []

    @lru_cache_with_ttl(maxsize=None, ttl=120)
    def request_rerank(self, query: str, texts: tuple[str]) -> List[str]:
        print("\n======Query=====")
        print(query)
        print("\n===========")
        print("documents pre results:")
        for hit in texts:
            print(hit)
            print("-----")
        try:
            rerank_hits = self.co.rerank(query=query, documents=list(texts), top_n=10, model="rerank-multilingual-v2.0")
            print("\n===========")
            print("ReRank results:")
            for hit in rerank_hits:
                print(texts[hit.index])
                print("-----")
        except Exception as error:
            print(error)
            return []

    @lru_cache_with_ttl(maxsize=None, ttl=120)
    def request_to_model_api(self, texts: tuple[str]) -> List[List[float]]:

        try:
            response = self.co.embed(
                model='embed-multilingual-light-v3.0',
                texts=list(texts),
                input_type='classification'
            )
            return response.embeddings
        except Exception as error:
            print(error)
            return []
