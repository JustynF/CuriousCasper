import nltk
from collections import defaultdict
import json


class Index:
    def __init__(self):

        self.index = defaultdict(list)
        self.documents = {}
        self.__unique_id = 0
        with open("./src/output/dictionary.json",'rb') as dict_file:
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
        for token in self.dict:
            token = token.encode("utf-8")
            if token in doc["title"].encode("utf-8") or token in doc["text"].encode("utf-8"):
                if doc["docId"] not in self.index[token]:
                    self.index[token].append(doc["docId"])
            self.documents[doc["docId"]] = doc

    def create_index(self):
        for doc in self.corpus:
            self.add(doc)

    def get_index(self):
        return self.index