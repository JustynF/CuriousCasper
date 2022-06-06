from nltk import bigrams,word_tokenize
from Helper.stopwords import remove_stopword as remove_stopwords
from collections import defaultdict
import json
import string

class BigramModel():
    def __init__(self):
        with open('output/uo_corpus.json') as corpus_file:
            uo_corpus = json.load(corpus_file)
        with open('output/reuters_corpus.json') as reuters_file:
            reuters_corpus = json.load(reuters_file)
            self.all_docs = [
                document for document in json.loads(uo_corpus)] + [document for document in reuters_corpus]

    def get_bigrams(self):
        bigram_model = defaultdict(lambda: defaultdict(lambda: 0))
        
        for document in self.all_docs:
            text = remove_stopwords([word.lower()
                                        for word in word_tokenize(document['text'])
                                        if word not in string.punctuation and 
                                        not any(i.isdigit() for i in word) and 
                                        word != ""])

            for w1, w2 in bigrams(text):
                bigram_model[w1][w2] += 1

            for w1 in bigram_model:
                w1_occurances = float(sum(bigram_model[w1].values()))
                for w2 in bigram_model[w1]:
                    bigram_model[w1][w2] /= w1_occurances

        with open('output/bigram_model.json', 'w') as outfile:
            json.dump(bigram_model, outfile, ensure_ascii=False, indent=4)
        return bigram_model