import json


class Access:
    def __init__(self):
        with open("./src/output/corpus.json", "r") as corpus_file:
            self.corpus = json.load(corpus_file)

    def get_document(self, docid):
        for doc in self.corpus:
            if doc['docId'] == docid:
                return doc

    def get_doc_ids(self):
        res=[]
        for doc in self.corpus:
            res.append(doc['docId'])
        return res

