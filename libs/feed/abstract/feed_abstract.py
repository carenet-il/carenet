from abc import ABC, abstractmethod
from typing import List

from libs.interfaces.document import Document


class FeedAbstract(ABC):

    @abstractmethod
    def pull(self) -> List[Document]:
        pass

    def __norm_document__(self, document) -> Document:
        pass
