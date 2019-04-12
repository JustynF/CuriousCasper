import json
import math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict

from src.Helper.stemmer import stemmer
from src.Helper.stopwords import remove_stopword
from src.Helper.normalization import normalize

class VectorSpaceModel():
    def __init__(self, inv_index,inv_index_freq):

        with open('src/output/corpus.json') as corpus:
            docs = json.load(corpus)

        self.all_doc_id = {document['docId'] for document in docs}
        self.inv_index = inv_index
        self.inv_index_freq = inv_index_freq

    def process_query(self, query, mode ='default'):

        query = query.lower()

        if mode == 'clean':
            query = normalize(stemmer(remove_stopword(query)))
        elif mode == 'normalize':
            query = normalize(query)
        elif mode == 'stemmer':
            query = stemmer(query)
        elif mode == 'stopwords':
            query = remove_stopword(query)

        tokens = word_tokenize(query)

        query_vec = [1] * len(tokens)

        idf_arr = get_idf(self.all_doc_id, self.inv_index)
        self.tf_idf_matrix = get_tf_idf(self.all_doc_id, self.inv_index, idf_arr, self.inv_index_freq)

        doc_vec = get_doc_vectors(self.all_doc_id, self.tf_idf_matrix, tokens)

        return get_scores(query_vec, doc_vec)


def get_idf(all_doc_id, inv_index):
    return {word: math.log10(len(all_doc_id) / len(docs)) for word, docs in inv_index.items()}


def get_tf_idf(all_doc_id, inv_index, idf_index, term_freq):
    tf_idf = defaultdict(lambda: defaultdict(int))
    for word, docs in inv_index.items():
        placeholder = defaultdict(int)
        for doc_id in all_doc_id:
            placeholder[doc_id] = 0

        for doc_id in docs:

            tf = term_freq[word][str(doc_id)] if str(doc_id) in term_freq[word].keys() else 0.0
            idf = idf_index[word]
            placeholder[doc_id] = tf * idf

        tf_idf[word] = placeholder

    return tf_idf


def get_doc_vectors(all_doc_id, tf_idf_matrix, tokens):

    doc_vec = defaultdict(tuple)

    for doc_id in all_doc_id:
        vector = []
        for token in tokens:
            doc_weights = tf_idf_matrix[token]
            weight = doc_weights[doc_id]
            vector.append(weight)
        doc_vec[doc_id] = vector

    return doc_vec


def get_scores(query_vector, doc_vectors):
    scores = []
    for doc_id, vector in doc_vectors.items():
        score = 0

        for query_vector_weight, doc_tf_idf in zip(query_vector, vector):
            score += query_vector_weight * doc_tf_idf
        scores.append((doc_id, score))

    scores.sort(key=lambda tup: tup[1], reverse=True)
    return [score for score in scores if score[1] != 0]