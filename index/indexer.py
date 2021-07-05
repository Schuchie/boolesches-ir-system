from typing import Dict, List
from tokenizer import Tok, TOK

from doc import Document
from .dictionary import Dictionary

import gensim.downloader as api
wv = api.load('word2vec-google-news-300')


class Indexer:
    ALLOWED_TOK_TYPES = [TOK.WORD, TOK.NUMBER, TOK.YEAR, TOK.DATE]
    docs: List[Document] = None
    dictionaries: List[Dictionary] = None

    doc_lengths: Dict[str, int] = None
    avg_doc_length = 0
    doc_vec_avg = None

    def __init__(self, docs: List[Document]):
        self.docs = docs
        self.dictionaries = {}
        self.doc_lengths = {}
        self.doc_vec_avg = {}

    def create(self):

        for doc in self.docs:
            position = 0
            doc_vec = []
            doc_vec_count = 0
            for term in doc.get_title():
                if len(term.txt) != 0 and term.kind in self.ALLOWED_TOK_TYPES:
                    word_embedding = self.get_word_embedding(term.txt)
                    if word_embedding is not None:
                        if len(doc_vec) == 0:
                            doc_vec = word_embedding
                        else:
                            doc_vec = self.add_n_vector(
                                doc_vec, word_embedding)
                        doc_vec_count += 1

                if self.add_term(term, doc.get_id(), position):
                    position += 1

            for term in doc.get_text():
                if len(term.txt) != 0 and term.kind in self.ALLOWED_TOK_TYPES:
                    word_embedding = self.get_word_embedding(term.txt)
                    if word_embedding is not None:
                        if len(doc_vec) == 0:
                            doc_vec = word_embedding
                        else:
                            doc_vec = self.add_n_vector(
                                doc_vec, word_embedding)
                        doc_vec_count += 1

                if self.add_term(term, doc.get_id(), position):
                    position += 1

            self.doc_vec_avg[doc.get_id()] = self.divide_const_n_vector(
                doc_vec, doc_vec_count)
            self.doc_lengths[doc.get_id()] = position
            self.avg_doc_length += position

        if len(self.doc_lengths) > 0:
            self.avg_doc_length = self.avg_doc_length / len(self.doc_lengths)

    def get_word_embedding(self, term: str):
        try:
            return wv[term]
        except KeyError:
            return None

    def add_n_vector(self, vec1, vec2):
        res = []
        for i in range(len(vec1)):
            res.append(vec1[i] + vec2[i])
        return res

    def divide_const_n_vector(self, vec, c):
        res = []
        for i in range(len(vec)):
            res.append(vec[i] / c)
        return res

    def add_term(self, token: Tok, doc_id: str, position: int) -> bool:

        if len(token.txt) != 0 and token.kind in self.ALLOWED_TOK_TYPES:
            dic = self.get_or_create_dictionary(token.txt)
            dic.add_posting_list(doc_id, position)
            return True

        return False

    def get_or_create_dictionary(self, term: str) -> Dictionary:

        if self.get_dictionary(term) is None:
            self.dictionaries[term] = Dictionary(term, len(self.docs))
        return self.get_dictionary(term)

    def get_dictionary(self, term: str) -> Dictionary:

        if term in self.dictionaries:
            return self.dictionaries[term]
        return None
