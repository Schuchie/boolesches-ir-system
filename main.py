from Metrics import Metrics
from query.word2vec import Word2Vec
from query.tf_idf import TdIdf
from query.query import Query
from click_shell import shell
import click

from doc import Document
from index import Indexer
from spell_check import SpellChecker


indexer = None
queries = None
q_rel = None
spell_checker = NotImplemented


@shell(prompt='wpp> ')
def main():
    global indexer, queries, q_rel, spell_checker

    docs = read_id_file_into_docs("docs.txt")
    queries = read_id_file_into_docs("queries.txt")
    q_rel = read_qrel_file("qrel.txt")
    # docs = read_file_into_docs("doc_dump.txt")
    # create_id_file_from_docs("ID.txt", docs)
    indexer = Indexer(docs)
    indexer.create()

    # 1. Parameter: Indexer
    # 2. Parameter: Jaccard threshold
    # 3. Parameter: k-Gram k
    # 4. Parameter: Limit corrected words
    spell_checker = SpellChecker(indexer, 0.7, 2, 3)


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
                elif len(data) == 3:
                    docs.append(Document(data[0], "", data[1], data[2]))
                else:
                    print("NoNoNo")
    return docs


def read_qrel_file(file):
    with open(file, 'r', encoding="utf8") as f:
        with click.progressbar(f.readlines(), label="Reading qrel") as bar:
            qrel_lines = bar

    res = {}

    for l in qrel_lines:
        splitted = l.split('\t')
        if not splitted[0] in res.keys():
            res[splitted[0]] = [splitted[2]]
        else:
            res[splitted[0]].append(splitted[2])

    return res


def create_id_file_from_docs(file, docs: "list[Document]"):

    with open(file, mode="w", encoding="utf-8") as f:
        for doc in docs:
            f.write(doc.get_id())
            f.write("\t")
            f.write(doc._title)
            f.write("\t")
            f.write(doc._text)
        f.close()


@main.command()
@click.argument('query_string', type=click.STRING)
def search(query_string):
    # example: "(blood OR pressure) AND cardiovascular"
    # example: "brown /2 development"
    # example: "(\"vegetable intake\" OR vegetable /2 intake OR vegetable /1 intake OR low) AND (deprivation OR bitterness)"
    query = Query(indexer)
    # 1. Parameter: Query
    # 2. Parameter: r threshold for found documents
    out, ms = query.parse(query_string, 1)

    if len(ms) > 0:
        for m in ms:
            possible_terms = spell_checker.check(m)

            if len(possible_terms) > 0:
                print(
                    f"{m} is possible wrong. Do you mean: {spell_checker.check(m)}")
            else:
                print(f"{m} is possible wrong.")

    click.echo(f"Suchanfrage: {out}\n")


@main.command()
@click.argument('term', type=click.STRING)
def check(term):
    global indexer

    if term in indexer.dictionaries:
        dic = indexer.dictionaries[term]
        click.echo(
            f"Term {term} has the idf score {dic.get_inverse_document_frequency()} and a total frequency of {dic.get_document_frequency()}")
    else:
        click.echo(f"Term {term} not found.")


@main.command()
@click.argument('term', type=click.STRING)
def score(term):
    global indexer

    tdidf = TdIdf(indexer)
    scores = tdidf.parse(term)

    rank = 1

    for (doc_id, score) in scores:
        if score <= 0:
            continue

        print(f"#{rank} {doc_id} with a score of: {score}")
        rank += 1


@main.command()
@click.argument('term', type=click.STRING)
def word2vec(term):
    global indexer

    word2vec = Word2Vec(indexer)
    scores = word2vec.parse(term)

    rank = 1

    for (doc_id, score) in scores:
        if rank > 100:
            break
        print(f"#{rank} {doc_id} with a score of: {score}")
        rank += 1


@main.command()
@click.argument('index', type=click.STRING)
def test(index):
    global queries, q_rel, indexer

    raw_query = ""

    for query in queries:
        if query.get_id() == index.lower():
            raw_query = query._title

    ground_truth = q_rel[index]
    ground_truth_len = len(ground_truth)

    tdidf = TdIdf(indexer)
    tdidf_res = tdidf.parse(raw_query)
    word2vec = Word2Vec(indexer)
    word2vec_res = word2vec.parse(raw_query)

    m = Metrics()
    r_precision = m.compute_r_score(tdidf_res[:ground_truth_len], ground_truth)
    w2v_r_precision = m.compute_r_score(
        word2vec_res[:ground_truth_len], ground_truth)

    print(f"td-idf (Top 5, r-precision={r_precision}):")
    test_output(index, tdidf_res, ground_truth, 5)
    print(f"word2vec (Top 5, r-precision={w2v_r_precision}):")
    test_output(index, word2vec_res, ground_truth, 5)

    print(f"td-idf (Top 10, r-precision={r_precision}):")
    test_output(index, tdidf_res, ground_truth, 10)
    print(f"word2vec (Top 10, r-precision={w2v_r_precision}):")
    test_output(index, word2vec_res, ground_truth, 10)

    print(f"td-idf (Top 20, r-precision={r_precision}):")
    test_output(index, tdidf_res, ground_truth, 20)
    print(f"word2vec (Top 20, r-precision={w2v_r_precision}):")
    test_output(index, word2vec_res, ground_truth, 20)

    print(f"td-idf (Top 50, r-precision={r_precision}):")
    test_output(index, tdidf_res, ground_truth, 50)
    print(f"word2vec (Top 50, r-precision={w2v_r_precision}):")
    test_output(index, word2vec_res, ground_truth, 50)


@main.command()
@click.argument('index', type=click.STRING)
def map(index):
    global queries, q_rel, indexer

    m = Metrics()

    test_query_indexes = ["plain-121", "plain-1021",
                          "plain-15", "plain-145", "1336"]
    test_queries = []

    td_idf_score = 0
    word_2_vec_score = 0

    for query in queries:
        if query.get_id() in test_query_indexes:
            test_queries.append((query.get_id(), query._title))

    for (index, q) in test_queries:
        ground_truth = q_rel[index.upper()]
        ground_truth_len = len(ground_truth)
        tdidf = TdIdf(indexer)
        tdidf_res = tdidf.parse(q)
        word2vec = Word2Vec(indexer)
        word2vec_res = word2vec.parse(q)

        td_idf_score += m.compute_p_score(
            tdidf_res[:ground_truth_len], ground_truth)
        word_2_vec_score += m.compute_p_score(
            word2vec_res[:ground_truth_len], ground_truth)

    print(
        f"MAP-Score of five test queries. td-idf: {td_idf_score / len(test_query_indexes)} word2vec: {word_2_vec_score / len(test_query_indexes)}")


def test_output(index, res, ground_truth, top_n=50):
    m = Metrics()

    precision_score = m.compute_p_score(res[:top_n], ground_truth)
    recall_score = m.compute_r_score(res[:top_n], ground_truth)
    f1_score = m.compute_f1_score(res[:top_n], ground_truth)

    print(
        f"scores for test-query {index} are p: {precision_score}, r: {recall_score}, f1: {f1_score}")


if __name__ == '__main__':
    main()
