from abstractpreprocess import AbstractPreProcess
import json
import requests
from bs4 import BeautifulSoup


class csiPreprocess(AbstractPreProcess):
    def __init__(self):
        super().__init__()
        self.url = "https://catalogue.uottawa.ca/en/courses/csi/"

    def preprocess(self):
        results = requests.get(self.url)
        data = BeautifulSoup(results.text, "html.parser")
        courseblocks = data.find_all('div', attrs={"class": "courseblock"})
        for i, courseblock in enumerate(courseblocks, 1):
            title = courseblock.find('p', attrs={'class': 'courseblocktitle'})
            desc = courseblock.find('p', attrs={'class': 'courseblockdesc'})
            if desc is not None:
                new_document = self.document(f'{i}', title.text, desc.text.strip())
            else:
                new_document = self.document(f'{i}', title.text, '')
            self.list.append(new_document)

        uniform_dicts = [list._asdict()
                         for list in self.list]

        with open('corpus.json', 'w', encoding="utf-8") as outfile:
            json.dump(uniform_dicts, outfile, ensure_ascii=False, indent=4)



def main():
    print("hi")

if __name__ == "__main__":
    main()