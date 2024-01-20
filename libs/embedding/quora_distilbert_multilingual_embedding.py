import os
from abc import ABC
from typing import List

import requests
from sentence_transformers import SentenceTransformer

from libs.embedding.abstract import EmbeddingAbstract


class QuoraDistilBertMultilingualEmbedding(EmbeddingAbstract, ABC):
    def __init__(self, load_locally_model=True):
        self.load_locally_model = load_locally_model

        if load_locally_model:
            self.model = SentenceTransformer(
                "sentence-transformers/quora-distilbert-multilingual"
            )
        pass

    def encode(self, text: str) -> List[float]:

        if self.load_locally_model:
            return self.model.encode(text).tolist()

        else:

            return self.request_to_model_api(text)

    def request_to_model_api(self, text):
        # do request to the api
        API_URL = "https://api-inference.huggingface.co/models/liranzxc/carenet-v2"
        headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        try:
            output = query({
                "inputs": text,
                "wait_for_model": True
            })
            return output
        except Exception as error:
            print(error)

            return []
