from query.bool_juncture import BoolJuncture
from query.phrase_query import PhraseQuery
from query.proximity_query import ProximityQuery
from index.indexer import Indexer
import re


class Query:
    indexer = None

    proximity = None
    phrase = None
    bool = None

    def __init__(self, indexer: Indexer):
        self.indexer = indexer
        self.proximity = ProximityQuery(indexer)
        self.phrase = PhraseQuery(indexer)
        self.bool = BoolJuncture(indexer)

    # r = if less than r documents are found return the term
    def parse(self, query: str, r=3):
        misspelled = []
        res, ms = self.process_proximity(query, r)
        misspelled += ms
        res, ms = self.process_phrase(res, r)
        misspelled += ms
        res, ms = self.bool.parse(res, r)
        misspelled += ms
        return res, misspelled

    def process_proximity(self, query: str, r: int):
        res = query
        q = re.findall(r"(\w*\d*)\s(\/\d+)\s(\w*\d*)", query, re.M | re.I)

        misspelled = []

        if q:
            for p in q:
                rawQuery = p[0] + " " + p[1] + " " + p[2]
                out, misspelled = self.proximity.parse(rawQuery, r)
                res = res.replace(rawQuery, str(out))
        return res, misspelled

    def process_phrase(self, query: str, r: int):
        res = query
        q = re.findall(r"\".*\"", query, re.M | re.I)

        misspelled = []

        if q:
            for p in q:
                out, misspelled = self.phrase.parse(p.replace('"', ""), r)
                res = res.replace(p, str(out))
        return res, misspelled
