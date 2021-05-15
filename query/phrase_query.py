from index.posting_list import PostingList
from index.dictionary import Dictionary
from index.indexer import Indexer


class PhraseQuery:
    indexer = None

    def __init__(self, indexer: Indexer):
        self.indexer = indexer

    def parse(self, query: str, maxOffset=1):
        phrases = query.split(" ")
        # Bad performance and bad programming... But simple
        if len(phrases) == 2:
            return self._parseTwo(phrases[0].strip(), phrases[1].strip(), maxOffset)
        if len(phrases) == 3:
            return self._parseThree(phrases[0].strip(), phrases[1].strip(), phrases[2].strip(), maxOffset)

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
                            if posTwo - posOne == maxOffset:
                                foundIndexes.append(idOne)

        return foundIndexes

    def _parseThree(self, wordOne: str, wordTwo: str, wordThree: str, maxOffset: int):
        dictOne = self.indexer.get_dictionary(wordOne)
        dictTwo = self.indexer.get_dictionary(wordTwo)
        dictThree = self.indexer.get_dictionary(wordThree)

        foundIndexes = []

        for idOne in dictOne.posting_lists:
            for idTwo in dictTwo.posting_lists:
                for idThree in dictThree.posting_lists:
                    if idOne == idTwo == idThree:
                        postingListOne = dictOne.posting_lists[idOne]
                        postingListTwo = dictTwo.posting_lists[idOne]
                        postingListThree = dictThree.posting_lists[idOne]
                        for posOne in postingListOne.get_positions():
                            for posTwo in postingListTwo.get_positions():
                                for posThree in postingListThree.get_positions():
                                    if posTwo - posOne == maxOffset and posThree - posTwo == maxOffset:
                                        foundIndexes.append(idOne)
        return foundIndexes
