import  nltk
from nltk import word_tokenize
from nltk.stem import *
from nltk.stem.porter import *
import json
from collections import namedtuple
from src.Helper.normalization import normalize as normalizer
from src.Helper.stemmer import stemmer as stemmer
from src.Helper.stopwords import remove_stopword as stopwords


class Dictionary:
    def __init__(self,mode):
        with open("src/output/corpus.json") as corpus_file:
            self.data = json.load(corpus_file)
        self.mode = "normalize"
        self.dict_text = self.get_doc_tokens()
        self.get_normalizer = normalizer
        self.get_stemmer = stemmer
        self.get_stopwords = stopwords


        self.tokens = self.get_tokens()

        self.alphaTokens = normalizer(self.tokens)
        self.stopTokens = stopwords(self.alphaTokens)
        self.stemTokens = stemmer(self.stopTokens)
        self.cleanTokens = stemmer(stopwords(self.alphaTokens))





    def create_dictionary(self):
        if (self.mode == "normalize"):
            words = self.alphaTokens
        elif self.mode == "stopwords":
            words = self.stopTokens
        elif self.mode == "stemmer":
            words = self.stemTokens
        elif self.mode == "clean":
            words = self.cleanTokens
        else:
            words = self.tokens

        with open("src/output/dictionary.json", 'wb') as outfile:
            json.dump(words, outfile, ensure_ascii=False, indent=4)
        return words

    def get_tokens(self):
        res = []
        for doc_id,text in self.dict_text.iteritems():
            res = res + text
        return res

    def get_doc_tokens(self):

        res = {}
        output = {}
        for doc in self.data:
            text_token = doc["text"]
            title_token = doc["title"]

            dict = title_token + " " + text_token

            res[doc["docId"]] = word_tokenize(dict.encode("UTF-8"))

            if self.mode == "normalize":
                output[doc["docId"]] = normalizer(word_tokenize(dict.encode("UTF-8")))
            elif self.mode == "stopwords":
                output[doc["docId"]] = stopwords(word_tokenize(dict.encode("UTF-8")))
            elif self.mode == "stemmer":
                output[doc["docId"]] = stemmer(word_tokenize(dict.encode("UTF-8")))
            elif self.mode == "clean":
                output[doc["docId"]] = stemmer(stopwords(normalizer(word_tokenize(dict.encode("UTF-8")))))
            else:
                output[doc["docId"]] = word_tokenize(dict.encode("UTF-8"))

        with open("src/output/doc_text.json", 'wb') as outfile:
            json.dump(output, outfile, ensure_ascii=False, indent=4)

        return res





