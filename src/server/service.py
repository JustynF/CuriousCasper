from src import access,stopwords,normalization,stemmer,csipreprocess,invertedindex,booleanretreival,dictionary

class Service:
    def __init__(self,n = None,s = None,stp = None):
        self.dict = self.create_dictionary(n,s,stp)
        self.index = self.create_inv_index()
        self.bool_model = self.create_bool_model()

    def create_corpus(self):
        corpus = csipreprocess.csiPreprocess()
        corpus.preprocess()

    def create_dictionary(self,normalizer,stem,stop):

        self.create_corpus()


        n = normalization.normalize if normalizer else None

        s = stemmer.stemmer if stem else None

        stp = stopwords.remove_stopword if stop else None

        d = dictionary.Dictionary(n,s,stp)
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





