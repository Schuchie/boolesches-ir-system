from index.posting_list import PostingList
from index.dictionary import Dictionary
from index.indexer import Indexer


class BoolJuncture:

    indexer = None

    def __init__(self, indexer: Indexer):
        self.indexer = indexer

    def parse(self, query: str):
        andConnections = query.split("OR")
        orPostingList = {}
        for andConnection in andConnections:
            terms = andConnection.strip().split("AND")
            andPostingList = {}
            for term in terms:
                dict = self.indexer.get_dictionary(term.strip())
                if dict is None:
                    andPostingList = self.merge_and(andPostingList, {})
                else:
                    if andPostingList == {}:
                        andPostingList = dict.posting_lists
                        continue

                    andPostingList = self.merge_and(
                        andPostingList, dict.posting_lists)
            orPostingList = self.merge_or(orPostingList, andPostingList)
        return orPostingList.keys()

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
