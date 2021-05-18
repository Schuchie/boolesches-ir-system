from doc.doc import Document
from index.posting_list import PostingList
from index.indexer import Indexer
import re
import ast


class BoolJuncture:

    indexer = None

    def __init__(self, indexer: Indexer):
        self.indexer = indexer

    def parse(self, query: str, r=3):
        orTerms = query.split("AND")
        andPostingList = {}
        possibleMisspelled = []
        for ors in orTerms:
            terms = ors.strip().replace("(", "").replace(")", "").split("OR")
            orPostingList = {}
            for term in terms:
                postingList, pm = self.get_index_list_from_term(term, r)
                possibleMisspelled += pm
                orPostingList = self.merge_or(orPostingList, postingList)

            if andPostingList == {}:
                andPostingList = orPostingList
            else:
                andPostingList = self.merge_and(andPostingList, orPostingList)
        return list(andPostingList.keys()), possibleMisspelled

    def get_index_list_from_term(self, term: str, r: int):
        # parse previous query results
        if re.match(r"\[.*\]", term.strip(), re.M | re.I):
            l = ast.literal_eval(term.strip())
            return self.list_to_dict(l), []
        # regular bool term
        if term.startswith("NOT"):
            res = {}
            strTerm = term.lstrip("NOT").strip()
            # get all docs without the term
            for doc in self.indexer.docs:
                if not self.doc_has_term(doc, strTerm):
                    res[doc.get_id()] = PostingList(0)
            return res, []

        dict = self.indexer.get_dictionary(term.strip())
        if dict is None:
            return {}, [term.strip()]

        if dict.frequency <= r:
            return dict.posting_lists, [term.strip()]
        return dict.posting_lists, []

    def merge_and(self, postingOne, postingTwo):
        newPostingList = {}
        for termOne in postingOne:
            for termTwo in postingTwo:
                if termOne == termTwo:
                    newPostingList[termOne] = postingOne[termOne]
        return newPostingList

    def merge_or(self, postingOne, postingTwo):
        newPostingList = postingOne.copy()
        for termTwo in postingTwo:
            if termTwo not in newPostingList:
                newPostingList[termTwo] = PostingList(0)
        return newPostingList

    def list_to_dict(self, list):
        out = {}
        for l in list:
            out[l] = PostingList(0)
        return out

    def doc_has_term(self, doc: Document, term: str):
        for t in doc.get_title():
            if t.txt == term:
                return True
        return False
