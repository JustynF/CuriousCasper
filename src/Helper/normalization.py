import nltk
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def normalize(tokens):

    alphaTokens = [t for t in tokens if re.match("^[a-zA-Z\d]+$",t)]
    alphaText = nltk.Text(alphaTokens)
    return alphaTokens