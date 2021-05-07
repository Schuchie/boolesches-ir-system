from doc import Document
from .dictionary import Dictionary


class Indexer:
    docs = None  # type: [Document]
    dictionaries = None

    def __init__(self, docs: [Document]):
        self.docs = docs
        self.dictionaries = {}

    def create(self):

        for doc in self.docs:
            position = 0
            for term in doc.get_title():
                self.add_term(term, doc.get_id(), position)
                position += 1
            for term in doc.get_text():
                self.add_term(term, doc.get_id(), position)
                position += 1

        print(self.dictionaries)

    def add_term(self, term: str, doc_id: str, position: int):
        dic = self.get_or_create_dictionary(term)

        dic.add_posting_list(doc_id, position)

    def get_or_create_dictionary(self, term: str):

        if term not in self.dictionaries:
            self.dictionaries[term] = Dictionary(term)
        return self.dictionaries[term]
