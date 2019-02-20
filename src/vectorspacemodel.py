import json
import math
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
import re

class VectorSpaceModel:

    def __init__(self, inv_index):
        self.complete_set = []
        with open("corpus.json", "r") as corpus_file:
            self.corpus = json.load(corpus_file)
        self.inverted_index = inv_index
        self.mode = 'original'
        self.idf_dict = [[]]

    def words(self, s):
        return re.findall(r"\w+", s, re.UNICODE | re.IGNORECASE)

    def calculate_idf(self, inverted_index):
        N = len(self.corpus)
        counts = Counter((w.lower() for e in self.corpus for w in self.words(e.get('text', ''))))
        self.idf_dict = counts.copy()
        for key in self.idf_dict:
            sample = self.idf_dict[key]
            self.idf_dict[key] = math.log10(1 + sample / N) + 1
        print(self.idf_dict)



