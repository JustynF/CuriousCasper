from src.Helper import stemmer, normalization, stopwords
from src.Modules.InvertedIndex import invertedindex
from src.Modules.Dictionary import dictionary
from src.Modules.Corpus import preprocess
from src.Modules.BooleanModel import booleanretreival


class Service:
    def __init__(self,mode):
        self.dict = self.create_dictionary(mode)
        self.index = self.create_inv_index()
        self.bool_model = self.create_bool_model()

    def create_corpus(self):
        corpus = preprocess.csiPreprocess()
        corpus.preprocess()

    def create_dictionary(self,mode):

        self.create_corpus()

        n = normalization.normalize if normalizer else None
        s = stemmer.stemmer if stem else None
        stp = stopwords.remove_stopword if stop else None

        d = dictionary.Dictionary(n, s, stp)
        d.create_dictionary()
        return d

    def create_inv_index(self):

        index = invertedindex.Index()
        index.create_index()
        inverted_index = index.get_index()

        return inverted_index

    def create_bool_model(self):
        bm = booleanretreival.BooleanModel(self.index)
        return bm

    def perform_query(self,query):
       return self.bool_model.process_query(query)





