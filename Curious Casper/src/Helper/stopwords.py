
#TODO Check default encoding methods ?
from nltk.corpus import stopwords

def remove_stopword(tokens,is_bool = False):
    # build a filtered list of tokens
    # import the stopwords
    stop_words = set(stopwords.words('english'))
    stop_words.update( set(stopwords.words('french')))
    stop_words.update(set(stopwords.words('spanish')))
    if is_bool:
        stop_words.remove("and")
        stop_words.remove("or")
        stop_words.remove("not")
        filtered_tokens = [t for t in [tokens] if t not in stop_words]
    else:
        filtered_tokens = [t for t in tokens if t not in stop_words]



    return filtered_tokens
