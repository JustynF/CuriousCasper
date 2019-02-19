import  nltk
from nltk import word_tokenize
from nltk.stem import *
from nltk.stem.porter import *
import re

def stemmer(tokens):
    stemmer = PorterStemmer()
    singles = [stemmer.stem(t) for t in tokens]
    print(singles)
    return singles