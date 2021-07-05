from typing import Dict
import math
from .posting_list import PostingList


class Dictionary:
    term: str = None
    frequency: int = 0
    posting_lists: Dict[str, PostingList] = None
    total_documents = 0

    def __init__(self, term: str, total_documents: int):
        self.term = term
        self.frequency = 0
        self.posting_lists = {}
        self.total_documents = total_documents

    def add_posting_list(self, doc_id: str, position: int):
        self.frequency += 1

        if doc_id not in self.posting_lists:
            posting_list = PostingList(position)
            self.posting_lists[doc_id] = posting_list

        else:
            posting_list = self.posting_lists[doc_id]
            posting_list.add_position(position)

        return posting_list

    # tf(t,d)
    def get_term_frequency(self, doc_id: str):
        if doc_id.lower() in self.posting_lists:
            return len(self.posting_lists[doc_id.lower()].get_positions())
        return 0

    # w(t,d)
    def get_normalized_term_frequency(self, doc_id: str):
        return self.get_term_frequency(doc_id) / self.total_documents

    # df(t)
    def get_document_frequency(self):
        return len(self.posting_lists)

    # idf(t)
    def get_inverse_document_frequency(self):
        idf = self.total_documents / self.get_document_frequency()
        return math.log10(idf)
