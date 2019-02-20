import booleanretreival as boolModel
from dictionary import Dictionary
import urllib2
import json

from stopwords import remove_stopword
from normalization import normalize
from stemmer import stemmer

def main():

  url = "https://catalogue.uottawa.ca/en/courses/csi/"
  resonse = urllib2.urlopen(url)
  raw = resonse.read().decode('utf8')

  with open("./src/corpus.json") as corpus_file:
    data = json.load(corpus_file)

  dict = Dictionary(data,normalize,stemmer,remove_stopword)
  print(type(dict.create_dictionary()))
if __name__== "__main__":
  main()