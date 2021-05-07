from doc import Document


class Indexer:

    def __init__(self, docs: [Document]):
        self.docs = docs

    def create(self):
        print("", len(self.docs))
        for doc in self.docs:
            print('Doc id', doc.get_id())
