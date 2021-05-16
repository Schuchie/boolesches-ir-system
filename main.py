from query.query import Query
from click_shell import shell
import click

from doc import Document
from index import Indexer


@shell(prompt='wpp> ')
def main():
    pass


def read_file_into_docs(file):
    docs = list()

    with open(file, mode="r", encoding="utf-8") as f:
        with click.progressbar(f.readlines(), label="Reading file") as bar:
            for l in bar:
                data = l.split("\t")
                if len(data) == 4:
                    docs.append(Document(data[0], data[1], data[2], data[3]))
                else:
                    print("NoNoNo")
    return docs


def read_id_file_into_docs(file):
    docs = list()

    with open(file, mode="r", encoding="utf-8") as f:
        with click.progressbar(f.readlines(), label="Reading file") as bar:
            for l in bar:
                data = l.split("\t")
                if len(data) == 2:
                    docs.append(Document(data[0], "", data[1], ""))
                else:
                    print("NoNoNo")
    return docs


def create_id_file_from_docs(file, docs: "list[Document]"):

    with open(file, mode="w", encoding="utf-8") as f:
        for doc in docs:
            f.write(doc.get_id())
            f.write("\t")
            f.write(doc._title)
            f.write("\n")
        f.close()


@main.command()
@click.argument('query_string', type=click.STRING)
def search(query_string):
    docs = read_id_file_into_docs("ID.txt")
    # docs = read_file_into_docs("doc_dump.txt")
    # create_id_file_from_docs("ID.txt", docs)
    indexer = Indexer(docs)
    indexer.create()

    # example: \"vegetable intake\" OR vegetable /2 intake OR vegetable /1 intake OR low AND deprivation OR bitterness
    query = Query(indexer)
    out = query.parse(query_string)
    click.echo(f"Suchanfrage: {out}")


if __name__ == '__main__':
    main()
