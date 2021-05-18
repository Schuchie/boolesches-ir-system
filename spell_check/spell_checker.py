import collections

from index.indexer import Indexer
from .k_gram_indexer import KGramIndexer
from .utils import jaccard, levenshtein_distance


class SpellChecker:
    j = None
    limit = None
    k_gram_indexer = None

    def __init__(self, indexer: Indexer, j=0.5, k=2, limit=3):
        self.k_gram_indexer = KGramIndexer(indexer, k)
        self.k_gram_indexer.parse()
        self.j = j
        self.limit = limit

    def check(self, term):
        dictionaries = self.k_gram_indexer.get_dictionaries_for_term(term)
        terms = set()

        for d in dictionaries:
            if jaccard(term, d.term) < self.j:
                continue

            terms.add(d.term)

        levenshtein_distances = {}

        for t in terms:
            levenshtein_distances[t] = levenshtein_distance(t, term)

        levenshtein_distances_sorted = collections.OrderedDict(
            sorted(
                levenshtein_distances.items(),
                key=lambda item: item[1],
            )
        )

        output = []

        # Limit results
        for i, (key, value) in enumerate(levenshtein_distances_sorted.items()):
            if i >= self.limit:
                break

            output.append(key)

        return output
