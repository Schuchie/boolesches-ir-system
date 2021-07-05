from doc.doc import Document
from index.indexer import Indexer
from numpy import dot
from numpy.linalg import norm


class Word2Vec:

    document_indexer: Indexer = None

    def __init__(self, indexer: Indexer):
        self.document_indexer = indexer

    def parse(self, query: str):
        query_document = Document("QUERY", "", query, "")
        query_indexer = Indexer([query_document])
        query_indexer.create()

        return self.calculate_word_2_vec(query_indexer.doc_vec_avg["query"])

    def calculate_word_2_vec(self, query_vec):
        result = []

        for doc in self.document_indexer.doc_vec_avg:
            vec_a = self.document_indexer.doc_vec_avg[doc]
            if len(vec_a) != len(query_vec):
                continue

            cos_sim = dot(vec_a, query_vec) / (norm(vec_a) * norm(query_vec))
            result.append((doc, cos_sim))

        return sorted(result, key=lambda x: x[1], reverse=True)
