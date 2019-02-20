import json
import math
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import os
import csv
from functools import reduce
import time

class VectorSpaceModel:

    def __init__(self):
        self.complete_set = []
        with open("corpus.json", "r") as corpus_file:
            self.corpus = json.load(corpus_file)

        self.mode = 'original'
        self.idf_dict = defaultdict(list)
        self.tf_idf_dict = defaultdict(lambda: defaultdict(int))

    def words(self, s):
        return re.findall(r"\w+", s, re.UNICODE | re.IGNORECASE)

    def calculate_idf(self, inverted_index):
        N = len(self.corpus)
        for word, docs in inverted_index.items():
            self.idf_dict[word].append(math.log10(N/len(docs)))
        return self.idf_dict.items()

    def calculate_tf_idf(self, inverted_index):
        for word, docs in inverted_index.items():
            temp = defaultdict(int)
            for doc in self.corpus:
                temp[doc] = 0
            for occurances in docs:
                temp[occurances.doc_id] = occurances.frequency * self.idf_dict[word]
            self.tf_idf_dict[word] = temp
        return self.tf_idf_dict.items()

