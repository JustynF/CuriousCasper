import  json
from nltk.tokenize import word_tokenize
from src.Helper.stemmer import stemmer
from src.Helper.stopwords import remove_stopword
from src.Helper.normalization import normalize
from os.path import dirname
import string
from math import log, sqrt
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

        self.dlt = self.get_dlt()



    def process_query(self, query, mode='default'):
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

        query_result = dict()
        for term in tokens:
            if term in self.inv_index_freq:
                doc_dict = self.inv_index_freq[term]  # retrieve index entry
                for docid, freq in doc_dict.iteritems():  # for each document and its word frequency
                    score = score_BM25(n=len(doc_dict), f=freq, qf=1, r=0, N=len(self.dlt),
                                       dl=self.dlt.get_length(docid),
                                       avdl=self.dlt.get_average_length())  # calculate score
                    if docid in query_result:  # this document has already been scored once
                        query_result[docid] += score
                    else:
                        query_result[docid] = score
        return query_result


    def get_dlt(self):
        dlt = DocumentLengthTable()
        for docid in self.doc_text:

            # build document length table
            length = len(self.doc_text[docid])
            dlt.add(docid, length)
        return dlt


k1 = 1.2
k2 = 100
b = 0.75
R = 0.0




def score_BM25(n, f, qf, r, N, dl, avdl):
    K = compute_K(dl, avdl)
    first = log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
    second = ((k1 + 1) * f) / (K + f)
    third = ((k2 + 1) * qf) / (k2 + qf)
    return first * second * third


def compute_K(dl, avdl):
    return k1 * ((1 - b) + b * (float(dl) / float(avdl)))

def getRelevantList(queryID, docList):
    file = open(CACM_REL, "r").read().splitlines()
    relList = []
    relDocs = []
    for line in file:
        values = line.split()
        if values[0] == str(queryID):
            relList.append(values[2])
    for doc in docList.keys():
        if doc in relList:
            relDocs.append(doc)
    return relDocs

def findRelDocMagnitude(docIndex):
    mag = 0
    for term in docIndex:
        mag += float(docIndex[term]**2)
        mag = float(sqrt(mag))
    return mag


def findNonRelDocMagnitude(docIndex):
    mag = 0
    for term in docIndex:
        mag += float(docIndex[term]**2)
    mag = float(sqrt(mag))
    return mag


def findRocchioScore(term, queryFreq, relDocMag, relIndex, nonRelMag, nonRelIndex):
    Q1 = ALPHA * queryFreq[term]
    Q2 = (BETA/relDocMag) * relIndex[term]
    Q3 = (GAMMA/nonRelMag) * nonRelIndex[term]
    rocchioScore = ALPHA * queryFreq[term] + (BETA/relDocMag) * relIndex[term] - (GAMMA/nonRelMag) * nonRelIndex[term]
    return rocchioScore


def findNewQuery(query, queryFreq, relDocMag, relIndex, nonRelMag, nonRelIndex, invertedIndex):
    updatedQuery = {}
    newQuery = query
    for term in invertedIndex:
        updatedQuery[term] = findRocchioScore(term, queryFreq, relDocMag, relIndex, nonRelMag, nonRelIndex)
    sortedUpdatedQuery = sorted(updatedQuery.items(), key=lambda x:x[1], reverse=True)
    if len(sortedUpdatedQuery)<20:
        loopRange = len(sortedUpdatedQuery)
    else:
        loopRange = 20
    for i in range(loopRange):
        term,frequency = sortedUpdatedQuery[i]
        if term not in query:
            newQuery +=  " "
            newQuery +=  term
    return newQuery


def pseudoRelevanceFeedbackScores(sortedBM25Score, query, invertedIndex, docLengths, relevant_list, queryID):
    global feedbackFlag
    feedbackFlag += 1
    newQuery = query
    k = 10 # top 10 documents to be taken as relevant
    queryFreq = queryFrequency(query, invertedIndex)
    relIndex = findDocs(k, sortedBM25Score, invertedIndex, "Relevant")
    relDocMag = findRelDocMagnitude(relIndex)
    nonRelIndex = findDocs(k, sortedBM25Score, invertedIndex, "Non-Relevant")
    nonRelMag = findNonRelDocMagnitude(nonRelIndex)
    newQuery = findNewQuery(query, queryFreq, relDocMag, relIndex, nonRelMag, nonRelIndex, invertedIndex)
    PseudoRelevanceScoreList = findDocumentsForQuery(newQuery, invertedIndex, docLengths, queryID)
    return PseudoRelevanceScoreList