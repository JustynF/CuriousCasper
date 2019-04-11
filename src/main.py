from src.Dictionary.dictionary import Dictionary

from src.CorpusAccess.access import Access
from src.Helper.stopwords import remove_stopword
from src.Helper.normalization import normalize
from src.Helper.stemmer import stemmer
from src.CorpusAccess.corpusaccess import csiPreprocess

from src.InvertedIndex.invertedindex import Index
from src.BooleanModel.booleanretreival import BooleanModel

def main():
  #Start of the Pipeline

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

  print(bm.process_query("solv*g"))


if __name__== "__main__":
  main()