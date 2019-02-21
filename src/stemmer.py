import  nltk
from nltk import word_tokenize
from nltk.stem import *
from nltk.stem.porter import *
import re

def stemmer(tokens):
    stemmer = PorterStemmer()
    if(type(tokens)==str):
        return stemmer.stem(str(tokens))
    return [stemmer.stem(t) for t in tokens]