from .posting import PostingList


class Dictionary:

    def __init__(self, term: str, frequency: int, posting_list: PostingList):
        self.term = term
        self.frequency = frequency
        self.posting_list = posting_list
