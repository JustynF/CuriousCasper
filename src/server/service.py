from src.Modules import booleanretreival
from src.Modules.Corpus import preprocess
from src.Modules.booleanretreival import BooleanModel
from src.Modules.vectorspacemodel import VectorSpaceModel
from src.Modules.bm25 import BM25
from src.Modules.Corpus.access import Access
import json
from os.path import dirname

directory = dirname(dirname(__file__))

class Service:
    def __init__(self):
        print "Service Started"

    def corpus_access(self, docid, corpus, topic=[]):
        ca = Access(corpus)
        if(type(docid)== set):
            docid = list(docid)
        return ca.get_documents(docid, topic)

    def get_doc(self, docid, corpus):
        ca = Access(corpus)

        return ca.get_doc(docid)

    def add_relevant_doc(self,docid,query,mode):
        ca = Access(mode)
        ca.add_relevant_doc(docid,query)

    def perfom_boolean_query(self,query,mode,corpus_mode):
        bm = BooleanModel(corpus_mode)
        return bm.process_query(query,mode)

    def perfom_vsm_query(self,query,mode,corpus_mode):
        vsm = VectorSpaceModel(corpus_mode)
        return vsm.process_query(query,mode)

    def perfom_bm25_query(self, query, mode, corpus_mode):
        bm25 = BM25(corpus_mode)
        return bm25.process_query(query, mode)

    def autocomplete(self, query):
        words = query.split(" ")
        if query.endswith(" "):
            word = words[len(words)-2]
        else:
            word = words[len(words)-1]

        with open(directory + '/output/bigram_model.json') as bigram_model:
            bigrams = json.load(bigram_model)

            if word not in bigrams:
                return []
            suggestions = bigrams[word]
            sorted_suggestions = sorted(suggestions.items(), key=lambda kv: kv[1], reverse=True)
            sorted_suggestions = sorted_suggestions[:(10 if len(
                sorted_suggestions) > 10 else len(sorted_suggestions) - 1)]

            results = []
            for key,_ in sorted_suggestions:
                results.append({'word':word,'suggestion':key})
            print(results)
            return results



