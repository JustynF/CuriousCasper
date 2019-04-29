import json
from os.path import dirname
class Access:
    def __init__(self,corpus_mode):
        directory = dirname(dirname(dirname(__file__)))
        if corpus_mode =='reuters':
            with open(directory + "/output/reuters_corpus.json", "r") as corpus_file:
                self.corpus = json.load(corpus_file)
        else:
            with open(directory + "/output/uo_corpus.json", "r") as corpus_file:
                self.corpus = json.load(corpus_file)
        with open(directory+"/output/knn_corpus_reuters.json", "r") as corpus_file:
            self.corpus_knn = json.load(corpus_file)

    def get_document(self, docids,topics=[],is_vsm=False):
        res = []

        if len(topics) != 0:
            docs = {doc["docId"]:doc for doc in self.corpus_knn}
            topics_set = set(topics)
            for doc_id in docids:
                if docs[doc_id]:
                    if docs[doc_id]["topic"] in topics_set:
                        docs[doc_id]["excerpt"] = docs[doc_id]["text"].split(". ")[0]
                        res.append(docs[doc_id])

        else:
            for doc in self.corpus:
                for doc_id in docids:
                 if str(doc["docId"]).decode('utf-8') == doc_id:
                      doc["excerpt"] = doc["text"].split(". ")[0]
                      res.append(doc)
        return res



    def get_doc_ids(self):
        res=[]
        for doc in self.corpus:
            res.append(doc['docId'])
        return res


