import json
import numpy as np
from nltk import word_tokenize,jaccard_distance,edit_distance
from collections import defaultdict,Counter
import operator
import time

class thesaurus():
    def __init__(self):
        with open('output/reuters_doc_text.json') as corpus:
            self.reuters_corpus = json.load(corpus)

        with open('output/reuters_tf.json') as reuters_tf:
            self.reuters_tf = json.load(reuters_tf)

    def build_thesaurus(self):
        terms = defaultdict(lambda: defaultdict(lambda: 0))
        total_term_frequency = defaultdict(int)



        for word, docs in self.reuters_tf.items():
            total = 0
            for doc_id in docs:
                #get term frequency for each word in document
                doc_id = doc_id
                total += self.reuters_tf[word][doc_id]
            total_term_frequency[word] = total

        #Outputing a sorted tuple of terms from dict got help from:
        #https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value

        sorted_dict = sorted(total_term_frequency.items(), key=operator.itemgetter(1),reverse=True)

        #ouput's an array of the top 1000 word tuples for each word and total frequency
        popular_words = [(word[0], word[1]) for word in sorted_dict][:1000]

        # words in corpus are not stemmed or normalized try using reuters_doc_text built  from corpus
        for doc,text in self.reuters_corpus.items():
            doc_id = doc
            text = text
            #find's the word count for each word in popular words for each document
            counted = Counter(text)
            for word_tuple in popular_words:
                word_count = counted[word_tuple[0]]
                if word_count > 0:
                    terms[doc_id][word_tuple[0]] = word_count

        #list of all the popular words
        popular_terms = [words[0] for words in popular_words]

        with open('output/thesaurus_tf.json', 'w') as outfile:
            json.dump(terms, outfile,
                      ensure_ascii=False, indent=4)

        with open('output/thesaurus_words.json', 'w') as outfile:
            json.dump(popular_terms, outfile, ensure_ascii=False, indent=4)

    #https: // python.gotrained.com / nltk - edit - distance - jaccard - distance /
    def calculate_similarity_scores(self):
        with open('output/thesaurus_tf.json') as term_freqs:
            thesaurus_tf = json.load(term_freqs)

        with open('output/thesaurus_words.json') as thesaurus_words:
            terms = json.load(thesaurus_words)

        new_thesaurus = defaultdict(lambda: defaultdict(lambda: 0))

        for i, w1 in enumerate(terms[:len(terms)-1]):
            for _,w2 in enumerate(terms[i+1:]):
                for doc_id,doc_terms in thesaurus_tf.items():
                    if w1 in doc_terms and w2 in doc_terms:
                        new_thesaurus[w1][w2] = jaccard(w1,w2)

        with open('output/thesaurus.json', 'w') as thesaurus:
            json.dump(new_thesaurus, thesaurus,
                      ensure_ascii=False, indent=4)


#https://www.python-course.eu/levenshtein_distance.php
def levenshtein(w1, w2):
    return edit_distance(w1,w2)

def jaccard(w1, w2):
    s1 = set(w1)
    s2 = set(w2)
    return jaccard_distance(s1,s2)



