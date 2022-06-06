import json
import math
from nltk.tokenize import word_tokenize
from collections import defaultdict
from Helper.stemmer import stemmer
from Helper.stopwords import remove_stopword
from Helper.normalization import normalize
import operator
from os.path import dirname
import string


class VectorSpaceModel():
    def __init__(self,corpus_mode = "default"):

        if corpus_mode == "reuters":
            with open(dirname(dirname(__file__))+'/output/reuters_corpus.json') as corpus:
                docs = json.load(corpus)
            with open(dirname(dirname(__file__)) + '/output/reuters_tf.json') as inv_index_freq:
                self.inv_index_freq = json.load(inv_index_freq)
            self.corpus_mode = corpus_mode
        else:
            with open(dirname(dirname(__file__))+'/output/uo_corpus.json') as corpus:
                docs = json.load(corpus)
            with open(dirname(dirname(__file__))+'/output/uo_tf.json') as inv_index_freq:
             self.inv_index_freq = json.load(inv_index_freq)

        with open(dirname(dirname(__file__))+'/output/thesaurus.json') as thesaurus:
            self.thesaurus = json.load(thesaurus)
        self.corpus_mode = corpus_mode
        self.all_doc_id = {document['docId'] for document in docs}
        self.tf_idf_matrix = get_tf_idf(self.get_idf(), self.inv_index_freq)

    def process_query(self, query, mode ='default'):
        print("processing VSM Query")
        query = [word for word in word_tokenize(query) if word not in string.punctuation]
        if (mode == "normalize"):
            query_tokens = normalize(query)
            query = " ".join(query_tokens)
        elif mode == "stopwords":
            query_tokens = remove_stopword(query)
            query = " ".join(query_tokens)
        elif mode == "stemmer":
            query_tokens = stemmer(query)
            query = " ".join(query_tokens)
        elif mode == "clean":
            query_tokens = normalize(stemmer(remove_stopword(query)))
            query = " ".join(query_tokens)

        tokens = word_tokenize(query)

        query_vec = [1] * len(tokens)

        expanded_tokens,expanded_vector = self.expand_query(tokens,query_vec)


        if self.corpus_mode == 'reuters':
            doc_vec = get_doc_vectors(self.all_doc_id, self.tf_idf_matrix, expanded_tokens)
            scores = get_scores(expanded_vector, doc_vec)
        else:
            doc_vec = get_doc_vectors(self.all_doc_id, self.tf_idf_matrix, tokens)
            scores = get_scores(query_vec, doc_vec)

        return scores

    def expand_query(self,tokens,vector):

        new_tokens = [token for token in tokens]
        new_vector = [vec for vec in vector]

        for token in tokens:
            #Check if the query is in the thesaurus
            if token not in self.thesaurus:
                continue
            #sort similar items by value
            synonyms = sorted(self.thesaurus[token].items(), key=operator.itemgetter(1))

            #get the two most similar words based on jaccard score
            if len(synonyms) > 2:
                synonyms = synonyms[:2]
            else:
                synonyms = synonyms[len(synonyms)-1]
            print ("Expanded query terms", synonyms)

            print(synonyms)
            for synonym, score in synonyms:
                #check if the query to be constructed already has the synonyms
                if synonym in new_tokens:
                    continue
                new_tokens.append(synonym)
                new_vector.append(score)



        return new_tokens,new_vector




    def get_idf(self):
        inv_index = self.inv_index_freq
        res = {word[0]: math.log10(len(self.all_doc_id)/len(word[1])) for word in inv_index.items()}
        return res



def get_tf_idf( idf_index, term_freq):
    tf_idf = defaultdict(lambda: defaultdict(int))

    for word in term_freq.items():
        for doc in word[1].items():
            tf_idf[word[0]][doc[0]] = idf_index[word[0]] * doc[1]
    return tf_idf


def get_doc_vectors(all_doc_id, tf_idf_matrix, tokens):

    doc_vec = defaultdict(tuple)

    for doc_id in all_doc_id:
        vector = []
        for token in tokens:
            doc_weights = tf_idf_matrix[token]
            weight = doc_weights[str(doc_id)]
            vector.append(weight)
        doc_vec[doc_id] = vector

    return doc_vec

def get_scores(query_vector, doc_vectors):
    scores = []
    for doc_id, vector in doc_vectors.items():
        score = 0

        #create and iterate over list of tuples
        for weight, doc_tf_idf in zip(query_vector, vector):
            score += weight * doc_tf_idf
        scores.append((doc_id, score))

    #sort scores from highest to lowest
    scores.sort(key=lambda tup: tup[1], reverse=True)
    return [score for score in scores if score[1] != 0]

