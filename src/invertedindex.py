import nltk
from collections import defaultdict
import json


class Index:
    def __init__(self):

        self.index = defaultdict(list)
        self.documents = {}
        self.__unique_id = 0
        with open("./src/output/dictionary.json") as dict_file:
            self.dict = json.load(dict_file)
        with open("./src/output/corpus.json") as corpus_file:
            self.corpus = json.load(corpus_file)

    def lookup(self, word):
        """
        Lookup a word in the index
        """
        word = word.lower()
        if self.stemmer:
            word = self.stemmer.stem(word)

        return [self.documents.get(id, None) for id in self.index.get(word)]

    def add(self, doc):
        """
        Add a document string to the index
        """
        for token in self.dict:
            if token in doc["title"] or token in doc["text"]:
                if doc["docId"] not in self.index[token.encode("utf-8")]:
                    self.index[token.encode("utf-8")].append(doc["docId"])
            self.documents[doc["docId"]] = doc

    def create_index(self):
        for doc in self.corpus:
            self.add(doc)

    def get_index(self):
        return self.index