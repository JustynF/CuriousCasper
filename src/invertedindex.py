import nltk
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer  # Assuming we're working with English


class Index:
    def __init__(self,dict):

        self.index = defaultdict(list)
        self.documents = {}
        self.__unique_id = 0
        self.dict = dict

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
