import nltk
import re

def normalize(tokens):
    alphaTokens = [t for t in tokens if re.match("^[a-zA-Z\d]+$",t)]
    alphaText = nltk.Text(alphaTokens)
    print(alphaTokens)
    return alphaTokens