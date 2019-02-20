import json
from csipreprocess import csiPreprocess
from vectorspacemodel import VectorSpaceModel
from dictionarybuilding import DictionaryBuilding

class Access:
    def __init__(self):
        with open("corpus.json", "r") as corpus_file:
            self.corpus = json.load(corpus_file)

    def corpus_access(self, docid):
        for doc in self.corpus:
            if doc['docID'] in docid:
                return doc

def main():
    x = {}
    test = VectorSpaceModel(x)
    test.calculate_idf()


if __name__ == "__main__":
    main()