import nltk


def remove_stopword(tokens):
    # build a filtered list of tokens
    nltk.download('stopwords')
    # import the stopwords
    from nltk.corpus import stopwords
    filtered_tokens = [t for t in tokens if t not in stopwords.words('english')]
    return filtered_tokens
