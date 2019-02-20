import nltk
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer  # Assuming we're working with English


class Index:
    def __init__(self, corpus,dict):

        self.index = defaultdict(list)
        self.documents = {}
        self.__unique_id = 0
        self.corpus = corpus
        self.dict = dict

    def lookup(self, word):
        """
        Lookup a word in the index
        """
        word = word.lower()
        if self.stemmer:
            word = self.stemmer.stem(word)

        return [self.documents.get(id, None) for id in self.index.get(word)]

    def add(self, document):
        """
        Add a document string to the index
        """
        for token in dict:

            if self.__unique_id not in self.index[token]:
                self.index[token].append(self.__unique_id)

        self.documents[self.__unique_id] = document
        self.__unique_id += 1


index = Index(nltk.word_tokenize,
              EnglishStemmer(),
              nltk.corpus.stopwords.words('english'))
