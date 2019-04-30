import  nltk
from nltk import word_tokenize

import json

import string
from os.path import dirname
import fuzzy
from collections import defaultdict
from src.Helper.stemmer import stemmer
from src.Helper.stopwords import remove_stopword
from src.Helper.normalization import normalize

dirpath = dirname(dirname(__file__))


class soundex:
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



    def get_edit_distance(self,word):
        soundex = fuzzy.Soundex(4)
        return soundex(word)


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