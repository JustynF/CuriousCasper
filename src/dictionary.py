import  nltk
from nltk import word_tokenize
from nltk.stem import *
from nltk.stem.porter import *
from stopwords import remove_stopword
from normalization import normalize
from stemmer import stemmer
import json

def create_dictionary(data):
    tokens = word_tokenize(str(data))

    alphaTokens = normalize(tokens)

    stopTokens = remove_stopword(alphaTokens)

    stemTokens =  stemmer(stopTokens)

    dict = set(stopTokens+stemTokens)
    filteredData = nltk.Text(stemTokens)

    print(dict)

    if "CSI" in dict:
        print("faggots")
    return filteredData






