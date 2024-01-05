from abc import ABC
from typing import List

from libs.feed.abstract.feed_abstract import FeedAbstract
from libs.interfaces.document import Document


class N12Feed(FeedAbstract, ABC):
    def pull(self) -> List[Document]:
        pass

    def __norm_document__(self, document) -> Document:
        pass
