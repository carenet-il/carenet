import os
import time
from abc import ABC
from typing import List
from libs.embedding.abstract import EmbeddingAbstract

import google.generativeai as genai

from libs.utils.cache import lru_cache_with_ttl


class GeminiMultiLingualEmbedding(EmbeddingAbstract, ABC):
    def __init__(self, load_locally_model=True):
        self.load_locally_model = load_locally_model
        api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        genai.configure(api_key=api_key)

    def encode_bulk(self, texts: List[str]) -> List[List[float]]:
        return self.request_to_model_api(tuple(texts))

    def encode(self, text: str) -> List[float]:
        results = self.request_to_model_api(tuple([text]))
        if len(results) > 0:
            return results[0]

        return []

    def request_rerank(self, query: str, texts: tuple[str]) -> List[str]:
        pass

    @lru_cache_with_ttl(maxsize=None, ttl=120)
    def request_to_model_api(self, texts: tuple[str]) -> List[List[float]]:
        retry = 3
        while retry > 0:
            try:
                result = genai.embed_content(
                    model="models/embedding-001",
                    content=list(texts),
                    task_type="retrieval_document",
                    title="Embedding of list of strings")

                embedding: List[List[float]] = result['embedding']
                return embedding
            except Exception as error:
                print(error)
                retry -= 1
                time.sleep(100)
        return []
