from .posting_list import PostingList


class Dictionary:
    term = None  # type: str
    frequency = 0  # type: int
    posting_lists = None

    def __init__(self, term: str):
        self.term = term
        self.frequency = 0
        self.posting_lists = {}

    def add_posting_list(self, doc_id: str, position: int):
        self.frequency += 1

        if doc_id not in self.posting_lists:
            posting_list = PostingList(position)
            self.posting_lists[doc_id] = posting_list

        else:
            posting_list = self.posting_lists[doc_id]
            posting_list.add_position(position)

        return posting_list
