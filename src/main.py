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
  inv_index_words = index.get_index()

  print(inv_index_words["problem"])

  bm = BooleanModel(inv_index_words)


  print(bm.process_query("Problem OR solving"))

  print("query")
  print(bm.process_query("solv*"))


if __name__== "__main__":
  main()