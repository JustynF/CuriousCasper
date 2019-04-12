import nltk
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



def remove_stopword(tokens):
    # build a filtered list of tokens
    nltk.download('stopwords')
    # import the stopwords
    from nltk.corpus import stopwords
    filtered_tokens = [t.decode("UTF-8") for t in tokens if t not in stopwords.words('english')]

    return filtered_tokens
