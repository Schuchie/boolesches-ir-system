class Document:
    def __init__(self, id, url, title, text):
        self.id = id.lower()
        self.url = url.lower()
        self.title = title.lower()
        self.text = text.lower()
