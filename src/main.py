from src.Modules.dictionary import Dictionary
from src.Modules.invertedindex import Index
from src.Modules.booleanretreival import BooleanModel
from src.Modules.vectorspacemodel import VectorSpaceModel
from src.Modules.thesaurus import thesaurus
from src.Modules.bigrammodel import BigramModel
from src.Modules.Corpus.preprocess import csiPreprocess
from src.Modules.Corpus.reuterspreprocess import reuterspreprocess
from src.Modules.textcategorization import textCategorization
from src.Modules.bm25 import BM25
from src.Modules.phraseindex import phraseindex
from src.Modules.soundex import soundex

import time

def main():
  #Start of the Pipeline
  mode = "clean"
  corpus_mode = "reuters"

  # #create corpus
  # start0 = time.time()
  # print "Creating Reuters corpus..."
  # reuters_corpus = reuterspreprocess()
  # reuters_corpus.preprocess()
  # end0 = time.time()
  # print "Finished creating Reuters corpus "+ str(end0-start0) + "\n"
  #
  # #Crete dictionary
  # start = time.time()
  # print "Creating Dictionary..."
  # dict = Dictionary(mode)
  # end = time.time()
  # print "Finished creating dictionary " +str(end-start) + "\n"
  #
  #create inverted index
  # start2 = time.time()
  # print "Creating Inverted Index..."
  # index = Index()
  # index.create_index()
  #
  # end2 = time.time()
  # print "Finished creating Inverted Index " + str(end2 - start2) + "\n"
  #
  start2 = time.time()
  print "Creating Phrase Index..."

  s = soundex()
  s.createSoundexIndex()
  end2 = time.time()
  print "Finished creating Phrase Index " + str(end2 - start2) + "\n"

  # print "Creating thesaurus..."
  # # print "Creating thesaurus..."
  # start3 = time.time()
  # #create thesaurus
  # t = thesaurus()
  # t.build_thesaurus()
  # end3 = time.time()
  # print "Finished creating thesaurus " + str(end3-start3) + "\n"
  #
  # print "Calculating similarity scores..."
  # start4 = time.time()
  # t.calculate_similarity_scores()
  # end4 = time.time()
  # print "Finished calculating Similarity score " + str(end4-start4) + "\n"
  #
  # #Create Bigram Model
  # start5 = time.time()
  # print "Creating Bigram Model..."
  # bigram = BigramModel()
  # bigram.get_bigrams()
  # end5 = time.time()
  # print "Finished calculating bigram model " + str(end5-start5) + "\n"
  #
  # #process knn
  # start = time.time()
  # print "Starting Text Categorization..."
  # knn = textCategorization()
  # knn.process()
  # end = time.time()
  #
  # print ("Finished Text Categorization ",str(end-start))
  #
  #create BooleanModel
  bm = BooleanModel(corpus_mode)

  print(bm.process_query("prob*",mode))

  print("Start processing VSM query...")
  start = time.time()
  #Create VectorSpaceModel
  vsm = VectorSpaceModel(corpus_mode)
  res = vsm.process_query("canada canola oil", mode)
  print (res)
  end = time.time()
  print("finished processing VSM query " + str(end - start))

  print("Start processing BM25 query...")
  start = time.time()
  bm25 = BM25(corpus_mode)
  print bm25.process_query("occidental", mode)
  end = time.time()
  print("finished processing BM25 query " + str(end - start))


if __name__== "__main__":
  main()