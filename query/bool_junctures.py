from index.posting_list import PostingList
from index.dictionary import Dictionary
from index.indexer import Indexer


class BoolJunctores:

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
                dict = self.findWord(term.strip())
                if andPostingList == {}:
                    andPostingList = dict.posting_lists
                    continue

                andPostingList = self.mergeAND(
                    andPostingList, dict.posting_lists)
            orPostingList = self.mergeOR(orPostingList, andPostingList)
        return orPostingList

    def findWord(self, word: str) -> Dictionary:
        if word in self.indexer.dictionaries:
            return self.indexer.dictionaries[word]
        else:
            return None

    def mergeAND(self, postingOne, postingTwo):
        newPostingList = {}
        for termOne in postingOne:
            for termTwo in postingTwo:
                if termOne == termTwo:
                    newPostingList[termOne] = PostingList(0)
        return newPostingList

    def mergeOR(self, postingOne, postingTwo):
        newPostingList = postingOne.copy()
        for termTwo in postingTwo:
            if termTwo not in newPostingList:
                newPostingList[termTwo] = PostingList(0)
        return newPostingList
