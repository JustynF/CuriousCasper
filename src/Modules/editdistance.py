import  nltk
from nltk import word_tokenize,edit_distance

import json

import string
from os.path import dirname
import fuzzy
from collections import defaultdict
from src.Helper.stemmer import stemmer
from src.Helper.stopwords import remove_stopword
from src.Helper.normalization import normalize

dirpath = dirname(dirname(__file__))


class editdistance:
    def __init__(self,mode = "default"):
        with open(dirpath+"/output/new_reuters_dict.json") as reuters_file:
            self.dict_reuters = json.load(reuters_file)
        with open(dirpath+"/output/new_uo_dict.json") as reuters_file:
            self.dict_uo = json.load(reuters_file)
        with open(dirpath+"/output/reuters_tf.json") as reuters_file:
            self.reuters_tf = json.load(reuters_file)
        with open(dirpath+"/output/uo_tf.json") as reuters_file:
            self.uo_tf = json.load(reuters_file)
        self.mode = mode



    def get_edit_distance(self,word,corpus):
        res = defaultdict()
        if corpus == 'reuters':
            dictionary = self.dict_reuters
        else:
            dictionary = self.dict_uo
        first_letter = word[:1]
        for term in dictionary:
            if term.startswith(first_letter):
                res[term] = levenshtein(term,word)


        return res


    def preprocess_query(self,query):
        mode = self.mode
        query = [word for word in word_tokenize(query) if word not in string.punctuation]
        if (mode == "normalize"):
            query_tokens = normalize(query, True)
            query = " ".join(query_tokens)
        elif mode == "stopwords":
            query_tokens = remove_stopword(query, True)
            query = " ".join(query_tokens)
        elif mode == "stemmer":
            query_tokens = stemmer(query)
            query = " ".join(query_tokens)
        elif mode == "clean":
            query_tokens = normalize(stemmer(remove_stopword(query, True)), True)
            query = " ".join(query_tokens)
        else:
            query_tokens = normalize(query, True)
            query = " ".join(query_tokens)

        return query_tokens


def levenshtein(s, t, costs=(1, 1, 2)):
    rows = len(s) + 1
    cols = len(t) + 1
    deletes, inserts, substitutes = costs

    dist = [[0 for x in range(cols)] for x in range(rows)]

    for row in range(1, rows):
        dist[row][0] = row * deletes

    for col in range(1, cols):
        dist[0][col] = col * inserts

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                cost = substitutes
            dist[row][col] = min(dist[row - 1][col] + deletes,
                                 dist[row][col - 1] + inserts,
                                 dist[row - 1][col - 1] + cost)  # substitution

    return dist[row][col]