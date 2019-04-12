import  nltk
from nltk import word_tokenize
from nltk.stem import *
from nltk.stem.porter import *
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def stemmer(tokens):
    stemmer = PorterStemmer()
    if(type(tokens)==str):
        return stemmer.stem(str(tokens))
    return [stemmer.stem(t) for t in tokens]