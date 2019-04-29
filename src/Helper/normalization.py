import nltk
import re


def normalize(tokens,is_bool = False):


    if is_bool:
     alphaTokens = [t for t in tokens if re.match("^[a-zA-Z*\d]+$", t)]
    else:
     alphaTokens = [re.sub("\.","",t) for t in tokens if (re.match("^[a-zA-Z\d]+$",t) or t.lower() == 'u.s.a') or t.lower() == 'u.s']
    return alphaTokens