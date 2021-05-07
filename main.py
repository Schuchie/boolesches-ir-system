import tokenize
import itertools
from io import BytesIO

from doc import Document


def main():
    docs = list()

    with open("doc_dump.txt", mode="r", encoding="utf-8") as f:
        for l in f.readlines():
            data = l.split("\t")
            if len(data) == 4:
                docs.append(Document(data[0], data[1], data[2], data[3]))
            else:
                print("NoNoNo")


if __name__ == '__main__':
    main()
