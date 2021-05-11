from tokenizer import Tok
from tokenizer import TOK

from doc import Document
from .dictionary import Dictionary


class Indexer:
    ALLOWED_TOK_TYPES = [TOK.WORD, TOK.NUMBER, TOK.YEAR, TOK.DATE]
    docs = None  # type: [Document]
    dictionaries = None

    def __init__(self, docs: [Document]):
        self.docs = docs
        self.dictionaries = {}

    def create(self):

        for doc in self.docs:
            position = 0
            for term in doc.get_title():
                if self.add_term(term, doc.get_id(), position):
                    position += 1
            for term in doc.get_text():
                if self.add_term(term, doc.get_id(), position):
                    position += 1

    def add_term(self, token: Tok, doc_id: str, position: int) -> bool:

        if len(token.txt) != 0 and token.kind in self.ALLOWED_TOK_TYPES:
            dic = self.get_or_create_dictionary(token.txt)
            dic.add_posting_list(doc_id, position)
            return True

        return False

    def get_or_create_dictionary(self, term: str):

        if term not in self.dictionaries:
            self.dictionaries[term] = Dictionary(term)
        return self.dictionaries[term]
