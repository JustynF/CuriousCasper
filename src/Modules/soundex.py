import  nltk
from nltk import word_tokenize
from nltk.stem import *
from nltk.stem.porter import *
import json
from collections import namedtuple
from src.Helper.rake import Rake
from rake_nltk import Rake as nltk_rake
from src.Helper.normalization import normalize as normalizer
from src.Helper.stemmer import stemmer as stemmer
from src.Helper.stopwords import remove_stopword as stopwords
from nltk.corpus import stopwords as set_stopwords
import string
from os.path import dirname
import fuzzy
from collections import defaultdict

dirpath = dirname(dirname(__file__))


class soundex:
    def __init__(self,mode = "default"):
        with open("src/output/new_reuters_dict.json") as reuters_file:
            self.dict_reuters = json.load(reuters_file)
        with open("src/output/new_uo_dict.json") as reuters_file:
            self.dict_uo = json.load(reuters_file)
        with open("src/output/reuters_tf.json") as reuters_file:
            self.reuters_tf = json.load(reuters_file)
        with open("src/output/uo_tf.json") as reuters_file:
            self.uo_tf = json.load(reuters_file)
        self.mode = mode


    def createSoundexIndex(self):
        res = defaultdict()

        soundex = fuzzy.Soundex(4)

        for word in self.dict_reuters:
            word = word.decode("utf-8")
            word_soundex = soundex(word)
            docs = self.reuters_tf[word]
            if word_soundex not in res:
                res[word_soundex] = {}

            res[word_soundex][word] = sum(docs.values())


        with open(dirpath+"/output/soundex.json","wb") as phrase_index:
            json.dump(res,phrase_index,ensure_ascii=False,indent=4)
        return res

