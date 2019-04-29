import nltk
from collections import defaultdict
import json
import re


class Index:
    def __init__(self):

        self.uo_index = defaultdict(list)
        self.uo_documents = {}

        self.reuters_index = defaultdict(list)
        self.reuters_documents = {}


        with open("src/output/uo_doc_text.json",'rb') as doc_text:
            self.uo_doc_text = json.load(doc_text)
        with open("src/output/uo_corpus.json") as corpus_file:
            self.uo_corpus = json.load(corpus_file)

        with open("src/output/reuters_doc_text.json",'rb') as doc_text:
            self.reuters_doc_text = json.load(doc_text)
        with open("src/output/reuters_corpus.json") as corpus_file:
            self.reuters_corpus = json.load(corpus_file)

        self.uo_doc_freq = {}
        self.reuters_doc_freq = {}


    def create_index(self):
        self.term_frequency()



    def term_frequency(self):
        print(" getting uo_term_frequency")
        for doc_id,text in self.uo_doc_text.iteritems():
            for token in text :
                token = token.encode("utf-8")
                id = doc_id.encode("utf-8")

                if token not in self.uo_doc_freq.keys():
                    self.uo_doc_freq[token] = {}
                self.uo_doc_freq[token][id] = text.count(token)

        print(" getting reuters_term_frequency")

        for doc_id, text in self.reuters_doc_text.iteritems():
            for token in text:
                token = token.encode("utf-8")
                id = doc_id.encode("utf-8")

                #Check if the token already has document if not initialze empty dict
                if token not in self.reuters_doc_freq.keys():
                    self.reuters_doc_freq[token] = {}
                self.reuters_doc_freq[token][id] = text.count(token)

        with open('src/output/uo_tf.json', 'w', ) as outfile:
            json.dump(self.uo_doc_freq, outfile, ensure_ascii=False, indent=4)

        with open('src/output/reuters_tf.json', 'w', ) as outfile:
            json.dump(self.reuters_doc_freq, outfile, ensure_ascii=False, indent=4)
