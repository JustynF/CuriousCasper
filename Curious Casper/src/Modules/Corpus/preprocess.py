import json
import requests
from bs4 import BeautifulSoup
from collections import namedtuple

class csiPreprocess():
    def __init__(self):
        self.url = "https://catalogue.uottawa.ca/en/courses/csi/"
        self.document = namedtuple("document","docId title text")
        self.courses = []

    def preprocess(self):

        results = requests.get(self.url)
        data = BeautifulSoup(results.text, "html.parser")
        courseblocks = data.find_all('div', attrs={"class": "courseblock"})
        for i, courseblock in enumerate(courseblocks, 1):
            title = courseblock.find('p', attrs={'class': 'courseblocktitle'})
            desc = courseblock.find('p', attrs={'class': 'courseblockdesc'})
            if desc is not None:
                new_document = {
                    "docId":i,
                    "title":title.text,
                    "text":desc.text.strip()
                }
                #new_document = self.document(i, title.text, desc.text.strip())
            else:
                new_document = {
                    "docId": i,
                    "title": title.text,
                    "text": "desc n/a"
                }
            self.courses.append(new_document)


        output = json.dumps(self.courses)

        with open('output/uo_corpus.json', 'w',) as outfile:
            json.dump(output, outfile)



def main():
    print("hi")

if __name__ == "__main__":
    main()