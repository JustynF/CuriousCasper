import booleanretreival as boolModel
import dictionary as dictionary
import urllib2
import json

def main():

  url = "https://catalogue.uottawa.ca/en/courses/csi/"
  resonse = urllib2.urlopen(url)
  raw = resonse.read().decode('utf8')

  with open("corpus.json") as corpus_file:
    data = json.load(corpus_file)

  print(dictionary.create_dictionary(data))

if __name__== "__main__":
  main()