import booleanretreival as boolModel
from dictionary import Dictionary
import json

from access import Access
from stopwords import remove_stopword
from normalization import normalize
from stemmer import stemmer
from csipreprocess import csiPreprocess

from invertedindex import Index

def main():

  #Corpus Preprocess
  corpus = csiPreprocess()
  corpus.preprocess()

  corpusaccess = Access()


  with open("./src/corpus.json") as corpus_file:
    data = json.load(corpus_file)
  dict = Dictionary(data,normalize,stemmer,remove_stopword)



  index = Index(dict.create_dictionary())

  for doc in data:
    index.add(doc)

  print(str(index.index))

if __name__== "__main__":
  main()