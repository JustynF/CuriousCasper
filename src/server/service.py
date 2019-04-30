from src.Modules import booleanretreival
from src.Modules.Corpus import preprocess
from src.Modules.booleanretreival import BooleanModel
from src.Modules.vectorspacemodel import VectorSpaceModel
from src.Modules.bm25 import BM25
from src.Modules.Corpus.access import Access
from src.Modules.soundex import soundex
import json
from os.path import dirname
from nltk import edit_distance
directory = dirname(dirname(__file__))

class Service:
    def __init__(self):
        print "Service Started"
        with open( directory+"/output/soundex.json") as soundex:
            self.suggestions = json.load(soundex)

        with open(directory+"/output/new_reuters_dict.json") as reuters_dict:
            self.reuters_dict = json.load(reuters_dict)

        with open(directory+"/output/new_uo_dict.json") as uo_dict:
            self.uo_dict = json.load(uo_dict)

        with open(directory+"/output/new_uo_dict.json") as uo_dict:
            self.uo_dict = json.load(uo_dict)

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

    def perform_soundex(self,query,corpus_mode):
        suggestions = self.suggestions

        if corpus_mode == "reuters":
            dictionary = self.reuters_dict
        else:
            dictionary = self.uo_dict

        s = soundex(corpus_mode)
        query_tokens = s.preprocess_query(query)
        res = []
        for word_token in query_tokens:
            if word_token not in dictionary:
                query_soundex = s.get_soundex(word_token)

                if query_soundex in suggestions:
                    query_suggestion = max(suggestions[query_soundex], key=lambda key: suggestions[query_soundex][key])
                    res.append(query_suggestion)
            else:
                res.append(word_token)

        corrected_query = " ".join(res)
        return corrected_query








    def editdistance(self,query,corpus_mode):
        s = soundex(corpus_mode)
        query_tokens = s.preprocess_query(query)

        for word in query_tokens:
            if word_token not in dictionary:



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



