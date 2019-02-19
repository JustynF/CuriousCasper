import  nltk
from nltk import word_tokenize
from nltk.stem import *
from nltk.stem.porter import *
from stopwords import remove_stopword
from normalization import normalize
import json

def create_dictionary(data):
    tokens = word_tokenize(str(data))
    tokenText = nltk.Text(tokens)
    alphaTokens = normalize(tokens)
    filteredText = nltk.Text(remove_stopword(alphaTokens))

    return filteredText






