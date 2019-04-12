import nltk
from collections import defaultdict
import json


class Index:
    def __init__(self):

        self.index = defaultdict(list)
        self.documents = {}
        self.__unique_id = 0
        with open("src/output/dictionary.json",'rb') as dict_file:
            self.dict = json.load(dict_file)
        with open("src/output/doc_text.json",'rb') as doc_text:
            self.doc_text = json.load(doc_text)
        with open("src/output/corpus.json") as corpus_file:
            self.corpus = json.load(corpus_file)
        self.doc_freq = {}

    def add(self, doc):
        for token in self.dict:
            token = token.encode("utf-8")
            if token in doc["title"].encode("utf-8") or token in doc["text"].encode("utf-8"):
                if doc["docId"] not in self.index[token]:
                    self.index[token].append(doc["docId"])

            self.documents[doc["docId"]] = doc["text"]



    def create_index(self):
        for doc in self.corpus:
            self.add(doc)
        self.term_frequency()
        with open('src/output/invertedindex.json', 'wb',) as outfile:
            json.dump(self.index, outfile, ensure_ascii=False, indent=4)

    def term_frequency(self):
        for doc_id,text in self.doc_text.iteritems():
            for token in text :
                token = token.encode("utf-8")
                id = doc_id.encode("utf-8")

                if token not in self.doc_freq.keys():
                    self.doc_freq[token] = {}
                self.doc_freq[token][doc_id.encode("utf-8")] = text.count(token)


    def get_index(self):
        return self.index

    def get_freq(self):
        return self.doc_freq