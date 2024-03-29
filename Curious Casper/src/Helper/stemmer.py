import importlib

import  nltk
from nltk import word_tokenize
from nltk.stem import *
from nltk.stem.porter import *
import re
import sys
importlib.reload(sys)
#sys.setdefaultencoding('utf-8')


def stemmer(tokens,is_bool = False):
    stemmer = PorterStemmer()
    if(type(tokens)==str):
        return stemmer.stem(str(tokens))

    return [stemmer.stem(t) for t in tokens]