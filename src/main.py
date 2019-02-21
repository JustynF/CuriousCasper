import booleanretreival as boolModel
from dictionary import Dictionary
import json

from access import Access
from stopwords import remove_stopword
from normalization import normalize
from stemmer import stemmer
from csipreprocess import csiPreprocess

from invertedindex import Index
from booleanretreival import BooleanModel

def main():

  #Corpus Preprocess
  corpus = csiPreprocess()
  corpus.preprocess()

  corpusaccess = Access()

  dict = Dictionary(normalize,stemmer,remove_stopword)

  dict.create_dictionary()

  index = Index()

  index.create_index()
  words = index.get_index()

  boolean_model = BooleanModel(words)



if __name__== "__main__":
  main()