import nltk
from collections import defaultdict
import json
import re

from os.path import dirname
directory = dirname(dirname(__file__))

class Index:
    def __init__(self):

        self.uo_index = defaultdict(list)
        self.uo_documents = {}

        self.reuters_index = defaultdict(list)
        self.reuters_documents = {}


        with open(directory+"/output/normalized/uo_doc_text.json",'rb') as doc_text:
            self.uo_doc_corpus = json.load(doc_text)
        with open(directory+"/output/normalized/new_uo_dict.json") as corpus_file:
            self.uo_dict = json.load(corpus_file)

        with open(directory+"/output/normalized/reuters_doc_text.json",'rb') as doc_text:
            self.reuters_corpus = json.load(doc_text)
        with open(directory+"/output/normalized/new_reuters_dict.json") as corpus_file:
            self.reuters_dict = json.load(corpus_file)

        self.uo_doc_freq = {}
        self.reuters_doc_freq = {}


    def create_index(self):
        self.term_frequency()



    def term_frequency(self):
        print(" getting uo_term_frequency")
        uo_tf= defaultdict()
        reuters_tf = defaultdict()
        for word in self.uo_dict:
            uo_tf[word] = {}
        for doc_id,text in self.uo_doc_corpus.iteritems():
            print doc_id
            for word in text:
                if doc_id not in uo_tf[word].keys():
                    uo_tf[word][doc_id] = 0
                uo_tf[word][doc_id] +=1

        with open(directory+'/output/normalized/test_uo_tf.json', 'w', ) as outfile:
            json.dump(uo_tf, outfile, ensure_ascii=False, indent=4)

        print(" getting reuters_term_frequency")

        for word in self.reuters_dict:
            reuters_tf[word] = {}
        for doc_id, text in self.reuters_corpus.iteritems():
            print doc_id
            for word  in text:
                if doc_id not in reuters_tf[word].keys():
                    reuters_tf[word][doc_id] = 0
                reuters_tf[word][doc_id]+=1


        with open(directory+'output/normalized/test_reuters_tf.json', 'w', ) as outfile:
            json.dump(reuters_tf, outfile, ensure_ascii=False, indent=4)
