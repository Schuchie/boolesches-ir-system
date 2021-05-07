import tokenize
import itertools
from io import BytesIO
import click

from doc import Document
from index import Indexer


@click.group(invoke_without_command=True)
def main():
    docs = read_file_into_docs("doc_dump.txt")
    create_id_file_from_docs("ID.txt", docs)
    indexer = Indexer(docs)
    indexer.create()


def read_file_into_docs(file):
    docs = list()

    with open(file, mode="r", encoding="utf-8") as f:
        for l in f.readlines():
            data = l.split("\t")
            if len(data) == 4:
                docs.append(Document(data[0], data[1], data[2], data[3]))
            else:
                print("NoNoNo")
    return docs


def create_id_file_from_docs(file, docs: [Document]):
    with open(file, mode="w", encoding="utf-8") as f:
        for doc in docs:
            f.write(doc.get_id())
            f.write("\t")
            f.write(doc.get_title()[1])
            f.write("\n")
        f.close()


@main.command()
@click.argument('query', nargs=-1, type=click.UNPROCESSED)
def search(query):
    click.echo(f"Suchanfrage: {query}")


if __name__ == '__main__':
    main()
