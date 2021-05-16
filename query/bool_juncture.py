from index.posting_list import PostingList
from index.indexer import Indexer
import re
import ast


class BoolJuncture:

    indexer = None

    def __init__(self, indexer: Indexer):
        self.indexer = indexer

    def parse(self, query: str):
        orTerms = query.split("AND")
        andPostingList = {}
        for ors in orTerms:
            terms = ors.strip().split("OR")
            orPostingList = {}
            for term in terms:
                postingList = self.get_posting_list_from_term(term)
                orPostingList = self.merge_or(orPostingList, postingList)

            andPostingList = self.merge_and(andPostingList, orPostingList)
        return list(orPostingList.keys())

    def get_posting_list_from_term(self, term):
        # parse previous query results
        if re.match(r"\[.*\]", term.strip(), re.M | re.I):
            l = ast.literal_eval(term.strip())
            return self.list_to_dict(l)
        # regular bool term
        dict = self.indexer.get_dictionary(term.strip())
        if dict is None:
            return {}
        return dict.posting_lists

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
