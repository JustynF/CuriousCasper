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
    def __init__(self,mode = "default"):
        with open("src/output/uo_corpus.json") as corpus_file:
            self.data_uo = json.load(corpus_file)
        with open("src/output/reuters_corpus.json") as reuters_file:
            self.data_reuters = json.load(reuters_file)
        self.mode = mode

        self.uo_dict_text = self.uo_doc_text()
        self.uo_get_normalizer = normalizer
        self.uo_get_stemmer = stemmer
        self.uo_get_stopwords = stopwords

        self.uo_tokens = []
        self.uo_normalized_words = []
        self.uo_removed_stopwords = []
        self.uo_stemmed_words = []
        self.uo_clean_words = []

        #reuters files
        self.reuters_dict_text = self.reuters_doc_text()

        self.reuters_tokens = []
        self.reuters_normalized_words = []
        self.reuters_removed_stopwords = []
        self.reuters_stemmed_words = []
        self.reuters_clean_words = []



    def create_dictionary(self):
        #create list of tokens in both uo and reuters corpus
        self.uo_tokens = self.uo_get_tokens()
        self.reuters_tokens = self.reuters_get_tokens()

        self.uo_normalized_words = normalizer(self.uo_tokens)
        self.reuters_normalized_words = normalizer(self.reuters_tokens)

        uo_words = set()
        reuters_words = set()

        if (self.mode == "normalize"):
            uo_words.update(self.uo_normalized_words)
            reuters_words.update(self.reuters_normalized_words)

        elif self.mode == "stopwords":
            self.uo_removed_stopwords = stopwords(self.uo_normalized_words)
            self.reuters_removed_stopwords = stopwords(self.reuters_normalized_words)

            uo_words.update([word.encode("UTF-8") for word in self.uo_removed_stopwords])
            reuters_words.update([word.encode("UTF-8") for word in self.reuters_removed_stopwords])
        elif self.mode == "stemmer":
            self.uo_stemmed_words = stemmer(self.uo_normalized_words)
            self.reuters_stemmed_words = stemmer(self.reuters_normalized_words)

            uo_words.update([word.encode("UTF-8") for word in self.uo_stemmed_words])
            reuters_words.update([word.encode("UTF-8") for word in self.reuters_stemmed_words])

        elif self.mode == "clean":
            self.uo_clean_words = stemmer(stopwords(self.uo_normalized_words))
            self.reuters_clean_words = stemmer(stopwords(self.reuters_normalized_words))

            uo_words.update([word.encode("UTF-8") for word in self.uo_clean_words])
            reuters_words.update([word.encode("UTF-8") for word in self.reuters_clean_words])
        else:
            uo_words.update([word.encode("UTF-8") for word in self.uo_normalized_words])
            reuters_words.update([word.encode("UTF-8") for word in self.reuters_normalized_words])

        with open("src/output/uo_dictionary.json", 'wb') as outfile:
            list_uo_words = list(uo_words)
            json.dump(list_uo_words, outfile, ensure_ascii=False, indent=4)

        with open("src/output/reuters_dictionary.json", 'wb') as outfile:
            list_reuters_words = list(reuters_words)
            json.dump(list_reuters_words, outfile, ensure_ascii=False, indent=4)

    # def uo_get_tokens(self):
    #     print(" getting uo_tokens")
    #     res = []
    #     for doc_id,text in self.uo_dict_text.iteritems():
    #         res = res + text
    #     print(" finished getting uo_tokens")
    #     return res

    def uo_doc_text(self):
        print(" getting uo_doc_text")
        res = {}
        output = {}
        dict_set = set()
        for doc in self.data_uo:
            text_token = doc["text"].lower()
            title_token = doc["title"].lower()
            dict = title_token + " " + text_token

            res[doc["docId"]] = word_tokenize(dict.encode("UTF-8"))

            if self.mode == "normalize":
                out = normalizer(word_tokenize(dict.encode("UTF-8")))
                dict_set.update(out)
                output[doc["docId"]] = normalizer(word_tokenize(dict.encode("UTF-8")))
            elif self.mode == "stopwords":
                out = normalizer(stopwords(normalizer(word_tokenize(dict.encode("UTF-8")))))
                dict_set.update(out)
                output[doc["docId"]] = out
            elif self.mode == "stemmer":
                out = normalizer(stemmer(word_tokenize(dict.encode("UTF-8"))))
                dict_set.update(out)
                output[doc["docId"]] = out
            elif self.mode == "clean":
                out = normalizer(stemmer(stopwords(normalizer(word_tokenize(dict.encode("UTF-8"))))))
                dict_set.update(out)
                output[doc["docId"]] = out
            else:
                out = normalizer(word_tokenize(dict.encode("UTF-8")))
                dict_set.update(out)
                output[doc["docId"]] = out

        with open("src/output/new_uo_dict.json", 'wb') as outfile:
            json.dump(list(dict_set), outfile, ensure_ascii=False, indent=4)

        with open("src/output/uo_doc_text.json", 'wb') as outfile:
            json.dump(output, outfile, ensure_ascii=False, indent=4)
        print(" finished getting uo_doc_text")
        return res

    # def reuters_get_tokens(self):
    #     print(" getting reuters_tokens")
    #     res = []
    #     #get doc id and text in doc text file key is docId text is array of words indoc text
    #     for doc_id,text in self.reuters_dict_text.iteritems():
    #         res = res + text
    #     print(" finished getting reuters_tokens")
    #     return res

    def reuters_doc_text(self):
        print(" getting reuters_doc_text")
        res = {}
        output = {}
        dict_set = set()
        for doc in self.data_reuters:
            text_token = doc["text"].lower()
            title_token = doc["title"].lower()

            dict = title_token + " " + text_token

            tokenized = word_tokenize(dict.encode("UTF-8"))
            res[doc["docId"]] = tokenized
            if self.mode == "normalize":
                out = normalizer(word_tokenize(dict.encode("UTF-8")))
                dict_set.update(out)
                output[doc["docId"]] = out
            elif self.mode == "stopwords":
                out = normalizer(stopwords(word_tokenize(dict.encode("UTF-8"))))
                dict_set.update(out)
                output[doc["docId"]] = out
            elif self.mode == "stemmer":
                out = normalizer(stemmer(word_tokenize(dict.encode("UTF-8"))))
                dict_set.update(out)
                output[doc["docId"]] = out
            elif self.mode == "clean":
                out = normalizer(stemmer(stopwords(word_tokenize(dict.encode("UTF-8")))))
                dict_set.update(out)
                output[doc["docId"]] = out
            else:
                out = normalizer(word_tokenize(dict.encode("UTF-8")))
                dict_set.update(out)
                output[doc["docId"]] = out

        with open("src/output/new_reuters_dict.json", 'wb') as outfile:
            json.dump(list(dict_set), outfile, ensure_ascii=False, indent=4)

        with open("src/output/reuters_doc_text.json", 'wb') as outfile:
            json.dump(output, outfile, ensure_ascii=False, indent=4)
        print(" finished getting reuters_doc_text")
        return res




