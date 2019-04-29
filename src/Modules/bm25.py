import  json
from nltk.tokenize import word_tokenize
from src.Helper.stemmer import stemmer
from src.Helper.stopwords import remove_stopword
from src.Helper.normalization import normalize
from os.path import dirname
import string
from math import log, sqrt
from collections import defaultdict

k1 = 1.2
k2 = 100
b = 0.75
ALPHA = 1
BETA = 0.75
GAMMA = 0.15


class DocumentLengthTable:

    def __init__(self):
        self.table = dict()

    def __len__(self):
        return len(self.table)

    def add(self, docid, length):
        self.table[docid] = length

    def get_length(self, docid):
        if docid in self.table:
            return self.table[docid]
        else:
            raise LookupError('%s not found in table' % str(docid))

    def get_average_length(self):
        sum = 0
        for length in self.table.itervalues():
            sum += length
        return float(sum) / float(len(self.table))

class BM25():
    def __init__(self,corpus_mode="default"):
        if corpus_mode == "reuters":
            with open(dirname(dirname(__file__))+'/output/reuters_corpus.json') as corpus:
                docs = json.load(corpus)
            with open(dirname(dirname(__file__)) + '/output/reuters_tf.json') as inv_index_freq:
                self.inv_index_freq = json.load(inv_index_freq)
            self.corpus_mode = corpus_mode
            with open(dirname(dirname(__file__))+'/output/reuters_doc_text.json') as doc_text:
                self.doc_text = json.load(doc_text)
        else:
            with open(dirname(dirname(__file__))+'/output/uo_corpus.json') as corpus:
                docs = json.load(corpus)
            self.corpus_mode = corpus_mode
            with open(dirname(dirname(__file__))+'/output/uo_tf.json') as inv_index_freq:
             self.inv_index_freq = json.load(inv_index_freq)

            with open(dirname(dirname(__file__))+'/output/uo_doc_text.json') as doc_text:
                self.doc_text = json.load(doc_text)

        with open(dirname(dirname(__file__)) + '/output/relevance_feedback.json') as rel_docs:
            self.rel_docs = json.load(rel_docs)

        self.dlt = self.get_dlt()



    def process_query(self, query, mode='default',feedback=False):
        self.mode = mode
        rel_docs = get_rel_docs(query,self.rel_docs)
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
        qf_list = compute_query_freq(tokens)
        query_result = dict()
        for term in tokens:
            if term in self.inv_index_freq:
                qf = qf_list[term]
                doc_dict = self.inv_index_freq[term]  # retrieve index entry
                r = compute_r(self.inv_index_freq[term],rel_docs)
                for docid, freq in doc_dict.iteritems():  # for each document and its word frequency
                    score = score_BM25(n=len(doc_dict), f=freq, qf=qf, r=r, N=len(self.dlt),
                                       dl=self.dlt.get_length(docid),
                                       avdl=self.dlt.get_average_length(),
                                       R=len(rel_docs))  # calculate score
                    if docid in query_result:  # this document has already been scored once
                        query_result[docid] += score
                    else:
                        query_result[docid] = score

        if not feedback:
            return self.pseudoRelevanceFeedbackScores(query_result,tokens)
        else:
            return query_result


    def get_dlt(self):
        dlt = DocumentLengthTable()
        for docid in self.doc_text:

            # build document length table
            length = len(self.doc_text[docid])
            dlt.add(docid, length)
        return dlt

    def pseudoRelevanceFeedbackScores(self,sortedBM25Score, query):

        queryFreq = compute_query_freq(query)
        relIndex = find_docs(sortedBM25Score, self.doc_text, "Relevant")
        relDocMag = find_doc_mag(relIndex)
        nonRelIndex = find_docs(sortedBM25Score, self.doc_text, "non-relevant")
        nonRelMag = find_doc_mag(nonRelIndex)
        newQuery = expand_query(query, queryFreq, relDocMag, relIndex, nonRelMag, nonRelIndex, self.inv_index_freq)
        PseudoRelevanceScoreList = self.process_query(newQuery.encode("utf-8"),mode=self.mode,feedback=True)
        return PseudoRelevanceScoreList



def score_BM25(n, f, qf, r, N, dl, avdl,R=0.0):
    K = compute_K(dl, avdl)
    first = log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
    second = ((k1 + 1) * f) / (K + f)
    third = ((k2 + 1) * qf) / (k2 + qf)
    return first * second * third


def compute_K(dl, avdl):
    return k1 * ((1 - b) + b * (float(dl) / float(avdl)))

def find_docs(sortedBM25Score, invertedIndex, relevancy):
    relIndex = defaultdict(lambda: 0)

    if relevancy == "Relevant":
        for doc,score in sortedBM25Score.items()[:5]:
            relIndex = compute_doc_count(doc, relIndex, invertedIndex)
        return relIndex
    else:
        for doc,score in sortedBM25Score.items()[6:]:
            relIndex = compute_doc_count(doc, relIndex, invertedIndex)
        return relIndex


def compute_doc_count(doc, new_inv_index, doc_text):
    for term in doc_text[doc]:
        if term in new_inv_index.keys():
            new_inv_index[term] += 1
        else:
            new_inv_index[term] = 1
    return new_inv_index

def compute_query_freq(query):
    queryFreq = defaultdict(lambda :0)
    for term in query:
        if term in queryFreq.keys():
            queryFreq[term] += 1
        else:
            queryFreq[term] = 1

    return queryFreq


def find_doc_mag(docIndex):
    mag = 0
    for term in docIndex:
        mag += float(docIndex[term]**2)
        mag = float(sqrt(mag))
    return mag


def compute_roccio(term, queryFreq, relDocMag, relIndex, nonRelMag, nonRelIndex):
    rocchio_score = ALPHA * queryFreq[term] + (BETA/relDocMag) * relIndex[term] - (GAMMA/nonRelMag) * nonRelIndex[term]
    return rocchio_score

def compute_r(doc_list,rel_doc_list):
    count = 0
    for doc in rel_doc_list.keys():
        if doc in doc_list:
            count+=1
    return count

def get_rel_docs(query,rel_list):
    if query in rel_list.keys():
        return rel_list[query]
    else:
        return {}
     
def expand_query(query, queryFreq, relDocMag, relIndex, nonRelMag, nonRelIndex, invertedIndex):
    updatedQuery = {}
    newQuery = query
    for term in invertedIndex:
        updatedQuery[term] = compute_roccio(term, queryFreq, relDocMag, relIndex, nonRelMag, nonRelIndex)
    sortedUpdatedQuery = sorted(updatedQuery.items(), key=lambda x:x[1], reverse=True)
    if len(sortedUpdatedQuery)<10:
        new_query_terms = len(sortedUpdatedQuery)
    else:
        new_query_terms = 10
    for term in sortedUpdatedQuery[:new_query_terms]:
        if term[0] not in query:
            newQuery.append(term[0])

    return " ".join(newQuery)



