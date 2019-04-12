from src.Modules.Dictionary.dictionary import Dictionary
from src.Modules.Corpus.preprocess import csiPreprocess

from src.Modules.InvertedIndex.invertedindex import Index
from src.Modules.BooleanModel.booleanretreival import BooleanModel
from src.Modules.VectorSpaceModel.vectorspacemodel import VectorSpaceModel
from src.Modules.Corpus.reuterspreprocess import reuterspreprocess

def main():
  #Start of the Pipeline

  #Corpus Preprocess
  corpus = csiPreprocess()
  corpus.preprocess()


  #Crete dictionary
  dict = Dictionary(mode="default")
  dict.create_dictionary()

  #create inverted index
  index = Index()
  index.create_index()

  inv_index_words = index.get_index()
  inv_index_freq = index.get_freq()

  print(inv_index_words["problem"])
  #create BooleanModel
  bm = BooleanModel(inv_index_words)
  print(bm.process_query("problem OR solving","default"))

  #Create VectorSpaceModel
  vsm = VectorSpaceModel(inv_index_words,inv_index_freq)

  print (vsm.process_query("analysis", "default"))

  #reuters preprocess
  r_corpus = reuterspreprocess()
  r_corpus.preprocess()



if __name__== "__main__":
  main()