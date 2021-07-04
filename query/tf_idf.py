from math import log10
from doc.doc import Document
from index.indexer import Indexer


class TdIdf:

    document_indexer: Indexer = None

    def __init__(self, indexer: Indexer):
        self.document_indexer = indexer

    def parse(self, query: str):
        query_document = Document("QUERY", "", query, "")
        query_indexer = Indexer([query_document])
        query_indexer.create()

        return self.fastCosineScore(query_indexer, 1.0)

    def ranking(self, query_indexer: Indexer, doc_id: str, k: float):
        res = 0
        d_avg = k * \
            (self.document_indexer.doc_lengths[doc_id] /
             self.document_indexer.avg_doc_length)

        for term in query_indexer.dictionaries:
            if term not in self.document_indexer.dictionaries:
                continue
            q_term_data = query_indexer.dictionaries[term]
            d_term_data = self.document_indexer.dictionaries[term]
            tq_term_frequency = q_term_data.get_term_frequency("QUERY")
            td_term_frequency = d_term_data.get_term_frequency(doc_id)
            t_doc_frequency = d_term_data.get_document_frequency()
            if t_doc_frequency <= 0:
                continue
            N = len(self.document_indexer.docs)

            res += tq_term_frequency * \
                (td_term_frequency / (td_term_frequency + d_avg)) * \
                log10(N / t_doc_frequency)
        return res

    def fastCosineScore(self, query_indexer: Indexer, k: float):
        res_list = []
        for doc in self.document_indexer.docs:
            res_list.append((doc.get_id(), self.ranking(
                query_indexer, doc.get_id(), k)))

        return sorted(res_list, key=lambda x: x[1], reverse=True)
