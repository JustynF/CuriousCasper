import json
from csipreprocess import csiPreprocess

class Access:
    def __init__(self):
        with open("./src/corpus.json", "r") as corpus_file:
            self.corpus = json.load(corpus_file)

    def corpus_access(self, docid):
        for doc in self.corpus:
            if doc['docId'] == docid:
                return doc['title']
