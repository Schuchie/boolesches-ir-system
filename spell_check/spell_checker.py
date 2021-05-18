from index.indexer import Indexer
from .k_gram_indexer import KGramIndexer
from .utils import jaccard


class SpellChecker:
    j = None
    k_gram_indexer = None

    def __init__(self, indexer: Indexer, j=0.5, k=2):
        self.j = j
        self.k_gram_indexer = KGramIndexer(indexer, k)
        self.k_gram_indexer.parse()

    def check(self, term):
        dictionaries = self.k_gram_indexer.get_dictionaries_for_term(term)
        terms = set()

        for dict in dictionaries:
            if jaccard(term, dict.term) < self.j:
                continue

            terms.add(dict.term)

        return list(terms)
