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

dirpath = dirname(dirname(__file__))


class phraseindex:
    def __init__(self,mode = "default"):
        with open("src/output/uo_corpus.json") as corpus_file:
            self.data_uo = json.load(corpus_file)
        with open("src/output/reuters_corpus.json") as reuters_file:
            self.data_reuters = json.load(reuters_file)
        self.mode = mode
        with open("src/output/new_reuters_dict.json") as reuters_file:
            self.dict_reuters = json.load(reuters_file)
        self.mode = mode
        with open("src/output/reuters_tf.json") as reuters_file:
            self.reuters_tf = json.load(reuters_file)
        with open("src/output/new_uo_dict.json") as reuters_file:
            self.dict_uo = json.load(reuters_file)
        with open("src/output/reuters_tf.json") as reuters_file:
            self.uo_tf = json.load(reuters_file)



    def createPhraseIndex(self):
        res = {}
        path = dirpath+"/Helper/SmartStoplist.txt"
        #r = Rake(path)
        r = nltk_rake(min_length=2,stopwords= set(set_stopwords.words('english')),punctuations=string.punctuation)
        for doc in self.data_reuters:
            text = doc["text"]
            doc_id = doc["docId"]
            #phrases = r.run(text)
            r.extract_keywords_from_text(text)
            phrases = r.get_ranked_phrases_with_scores()

            res.update({str(phrase[1]):{doc_id:phrase[0]} for phrase in phrases})

        for doc in self.data_uo:
            text = doc["text"]
           # phrases = r.run(text)
            r.extract_keywords_from_text(text)
            phrases = r.get_ranked_phrases_with_scores()
            doc_id = doc["docId"]
            res.update({phrase[1]:{doc_id:phrase[0]} for phrase in phrases})


        with open(dirpath+"/output/phraseindex2.json","wb") as phrase_index:
            json.dump(res,phrase_index,ensure_ascii=False,indent=4)
        return res

