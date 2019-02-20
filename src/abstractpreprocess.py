from collections import namedtuple
from abc import ABC, abstractmethod


class AbstractPreProcess(ABC):

    def __init__(self):
        self.document = namedtuple("document", "docID title text")
        self.list = []
        super().__init__()

    @abstractmethod
    def preprocess(self):
        pass

