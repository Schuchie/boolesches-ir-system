from index.indexer import Indexer
import re


class ProximityQuery:
    indexer = None

    def __init__(self, indexer: Indexer):
        self.indexer = indexer

    def parse(self, query: str):
        q = re.match("(.*) (\/\d) (.*)", query, re.M | re.I)

        if q:
            wordOne = q.group(1)
            offset = q.group(2).replace("/", "")
            wordTwo = q.group(3)
            return self._parseTwo(wordOne.strip(), wordTwo.strip(), int(offset))

        return None

    def _parseTwo(self, wordOne: str, wordTwo: str, maxOffset: int):
        dictOne = self.indexer.get_dictionary(wordOne)
        dictTwo = self.indexer.get_dictionary(wordTwo)

        foundIndexes = []

        for idOne in dictOne.posting_lists:
            for idTwo in dictTwo.posting_lists:
                if idOne == idTwo:
                    postingListOne = dictOne.posting_lists[idOne]
                    postingListTwo = dictTwo.posting_lists[idOne]
                    for posOne in postingListOne.get_positions():
                        for posTwo in postingListTwo.get_positions():
                            if posTwo - posOne <= maxOffset:
                                foundIndexes.append(idOne)

        return foundIndexes
