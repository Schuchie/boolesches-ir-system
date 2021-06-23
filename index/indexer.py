from tokenizer import Tok, TOK

from doc import Document
from .dictionary import Dictionary


class Indexer:
    ALLOWED_TOK_TYPES = [TOK.WORD, TOK.NUMBER, TOK.YEAR, TOK.DATE]
    docs = None  # type: [Document]
    dictionaries = None

    def __init__(self, docs: "list[Document]"):
        self.docs = docs
        self.dictionaries = {}

    def create(self):

        for doc in self.docs:
            position = 0
            for term in doc.get_title():
                if self.add_term(term, doc.get_id(), position):
                    position += 1
            # for term in doc.get_text():
            #     if self.add_term(term, doc.get_id(), position):
            #         position += 1

    def add_term(self, token: Tok, doc_id: str, position: int) -> bool:

        if len(token.txt) != 0 and token.kind in self.ALLOWED_TOK_TYPES:
            dic = self.get_or_create_dictionary(token.txt)
            dic.add_posting_list(doc_id, position)
            return True

        return False

    def get_or_create_dictionary(self, term: str) -> Dictionary:

        if self.get_dictionary(term) is None:
            self.dictionaries[term] = Dictionary(term)
        return self.get_dictionary(term)

    def get_dictionary(self, term: str) -> Dictionary:

        if term in self.dictionaries:
            return self.dictionaries[term]
        return None
