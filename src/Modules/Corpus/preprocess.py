import json
import requests
from bs4 import BeautifulSoup
from collections import namedtuple

class csiPreprocess():
    def __init__(self):
        self.url = "https://catalogue.uottawa.ca/en/courses/csi/"
        self.document = namedtuple("document","docId title text")
        self.list = []

    def preprocess(self):

        results = requests.get(self.url)
        data = BeautifulSoup(results.text, "html.parser")
        courseblocks = data.find_all('div', attrs={"class": "courseblock"})
        for i, courseblock in enumerate(courseblocks, 1):
            title = courseblock.find('p', attrs={'class': 'courseblocktitle'})
            desc = courseblock.find('p', attrs={'class': 'courseblockdesc'})
            if desc is not None:
                new_document = self.document(i, title.text.encode('utf-8'), desc.text.encode('utf-8').strip())
            else:
                new_document = self.document(i, title.text.encode('utf-8'), '')
            self.list.append(new_document)

        output = [list._asdict()
                         for list in self.list]

        with open('src/output/uo_corpus.json', 'wb',) as outfile:
            json.dump(output, outfile, ensure_ascii=False, indent=4)



def main():
    print("hi")

if __name__ == "__main__":
    main()