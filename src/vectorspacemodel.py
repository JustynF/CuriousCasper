import collections
import json
import math
from collections import Counter, defaultdict

import re


class VectorSpaceModel:

    def __init__(self):
        self.complete_set = []
        with open("corpus.json", "r") as corpus_file:
            self.corpus = json.load(corpus_file)

        self.idf_dict = {}
        self.tf_idf_dict = defaultdict(lambda: defaultdict(int))

    def words(self, s):
        ''' Ignore, used for testing'''
        number_of_occurences = 0
        for word in s.split():
            if word == 'a':
                number_of_occurences += 1

    def calculate_idf(self, inverted_index):
        ''' Calculates the idf of all words and returns a list'''
        N = len(self.corpus)
        for word, docs in inverted_index.iteritems():
            self.idf_dict[word] = math.log10(N/len(docs))
        print(len(self.idf_dict))
        return self.idf_dict.items()

    def count(self, word, docId):
        ''' Counts number of occurances for a given word in a given document'''
        cnt = 0
        strnew = self.get_document(docId)
        strnew = strnew['text']
        for elem in strnew:
            if elem == word:
                cnt += 1
        return cnt

    def get_document(self, docId):
        ''' Returns a document given docId'''
        for doc in self.corpus:
            if doc['docId'] == docId:
                return doc


    def calculate_tf_idf(self, inverted_index, idf_index):
        ''' Calculates tfidf'''
        tf_idf = defaultdict(lambda: defaultdict(int))
        for words, docs in inverted_index.iteritems():
            placeholder = defaultdict(int)
            for occurance in docs:
                placeholder[words] = self.count(words, occurance) * self.idf_dict[words]
            tf_idf[words] = placeholder

        return tf_idf

    def calculate_doc_vecs(self, tf_idf_matrix, tokens):
        ''' Calculates doc vectors per document given a set of tokens'''
        doc_vecs = defaultdict(tuple)
        for doc_id in self.corpus:
            vector = []
            for token in tokens:
                doc_weights = tf_idf_matrix[token]
                weight = tf_idf_matrix[doc_id['docId']]
                vector.append(weight)
            doc_vecs[doc_id['docId']] = vector
        return doc_vecs


    def calculate_vec_score(self,query_vector, doc_vecs):
        ''' Sets up scores for each document dependant on the query given'''
        scores = []
        for doc_id, vector in doc_vecs:
            score = 0
            for terms, doc_tf_idf in query_vector:
                score += terms * doc_tf_idf
            scores.append((doc_id, score))
        return scores



