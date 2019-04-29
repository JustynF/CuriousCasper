import os
from bs4 import BeautifulSoup
import json
from collections import namedtuple

import re
import requests

class reuterspreprocess():

    def __init__(self):
        self.reuters_files = os.path.join(os.getcwd(), "src/reuters")
        self.document = namedtuple("document","docId title text topic")
        self.corpus_list = []

    def preprocess(self):
        for filename in os.listdir(self.reuters_files):
            if not filename.startswith('.'):
                with open(os.path.join(self.reuters_files, filename), 'r') as file:

                    data = file.read()
                    soup = BeautifulSoup(data, "html.parser")
                    docs = soup.find_all('reuters')

                    for index, doc in enumerate(docs, 1):
                        title = doc.find('title').text if doc.find('title') is not None else ""
                        text = doc.find('body').text if doc.find('body') is not None else ""
                        if text == "":
                           continue
                        doc_id = filename[:-4]+"-"+str(index)

                        #Adde topic to the document tuple for topic restriction and text categorization with KNN
                        topic = doc.find('topics').find_all("d")[0].text if doc.find(
                            'topics').find("d") is not None else ""
                        new_document = self.document(doc_id,title,text.replace('\n'," "),topic)

                        self.corpus_list.append(new_document)

        output = [corpus._asdict()
                         for corpus in self.corpus_list]

        with open('src/output/reuters_corpus.json', 'w') as outfile:
            json.dump(output, outfile, ensure_ascii=False, indent=4)
