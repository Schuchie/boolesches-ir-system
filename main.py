from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
from io import BytesIO


def main():
    f = open("doc_dump.txt", mode="r", encoding="utf-8")
    content = f.readlines()
    print(len(content))


if __name__ == '__main__':
    main()
