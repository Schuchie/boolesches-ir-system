from index.indexer import Indexer

from .utils import k_split


class KGramIndexer:
    k = None
    k_grams = {}
    indexer = None

    def __init__(self, indexer: Indexer, k=2):
        self.k = k
        self.indexer = indexer

    def parse(self):
        dictionaries = self.indexer.dictionaries

        for term in dictionaries:
            for split in k_split(term, self.k):
                if split not in self.k_grams:
                    self.k_grams[split] = []

                self.k_grams[split].append(dictionaries[term])
