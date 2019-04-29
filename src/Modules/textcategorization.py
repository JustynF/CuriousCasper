import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re
import numpy as np
import json

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

#used the text categorizatoin algorithm from
#https://appliedmachinelearning.blog/2018/01/18/conventional-approach-to-text-classification-clustering-using-k-nearest-neighbor-k-means-python-implementation/
class textCategorization():
    def __init__(self):
        with open('src/output/reuters_corpus.json') as corpus:
            self.reuters_corpus = json.load(corpus)
        self.training = [doc for doc in self.reuters_corpus if doc["topic"] != ""]
        self.test = [doc for doc in self.reuters_corpus if doc["topic"] == ""]
        self.topic_labels = list(set(doc["topic"] for doc in self.reuters_corpus if doc["topic"] != ""))
        self.labels = {label: index for index, label in enumerate(self.topic_labels)}
        with open('src/output/reuters_doc_text.json') as reuters_doc_text:
            self.reuters_doc_text = json.load(reuters_doc_text)

    def process(self):
        create_tfidf_vec = TfidfVectorizer(stop_words='english')

        X = create_tfidf_vec.fit_transform(
            [clean(doc["text"]) for doc in self.training])
        y_training = np.fromiter([
            self.labels[doc["topic"]] for doc in self.training], int)
        model = KNeighborsClassifier(n_neighbors=5, metric="euclidean")
        model.fit(X, y_training)

        test_set_lookup = {doc["docId"]: clean(
            doc["text"]) for doc in self.test}
        Test = create_tfidf_vec.transform(test_set_lookup.values())
        predicted_labels_knn = model.predict(Test)

        updated_docs = []
        list_topics = []
        for index, doc in enumerate(self.test):
            doc["topic"] = self.topic_labels[np.int(
                predicted_labels_knn[index])]
            list_topics.append(self.topic_labels[np.int(
                predicted_labels_knn[index])])
            updated_docs.append(doc)

        with open('src/output/knn_corpus_reuters.json', 'w') as outfile:
            json.dump(self.training + updated_docs,
                      outfile, ensure_ascii=False, indent=4)

        with open('src/output/knn_reuters.json', 'w') as outfile:
            json.dump(updated_docs,
                      outfile, ensure_ascii=False, indent=4)
        with open('src/output/topics.json','w') as outfile:
            json.dump(list(set(list_topics)),outfile, ensure_ascii=False, indent=4)

#Taken from clean seaction
#https://appliedmachinelearning.blog/2018/01/18/conventional-approach-to-text-classification-clustering-using-k-nearest-neighbor-k-means-python-implementation/
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word)
                          for word in punc_free.split())
    processed = re.sub(r"\d+", "", normalized)
    return processed