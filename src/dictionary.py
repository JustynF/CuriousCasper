import  nltk
from nltk import word_tokenize
from nltk.stem import *
from nltk.stem.porter import *
import json

class Dictionary:
    def __init__(self,normalizer= None, stemmer = None, stopwords = None):
        with open("./src/corpus.json") as corpus_file:
            self.data = json.load(corpus_file)

        self.get_normalizer = normalizer
        self.get_stemmer = stemmer
        self.get_stopwords = stopwords

        self.tokens = word_tokenize(str(self.data))

        if not self.get_normalizer:
            self.alphaTokens = self.tokens
        else:
            self.alphaTokens = normalizer(self.tokens)

        if not self.get_stopwords:
            self.stopTokens = self.alphaTokens
        else:
            self.stopTokens = stopwords(self.alphaTokens)

        if not self.get_stemmer:
            self.stemTokens = self.stopTokens
        else:
            self.stemTokens = stemmer(self.stopTokens)

    def create_dictionary(self):
        res = self.stemTokens
        with open("./src/output/dictionary.json", 'wb') as outfile:
            json.dump(res, outfile)
        return res




