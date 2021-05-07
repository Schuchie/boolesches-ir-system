class Document:
    def __init__(self, id, url, title, text):
        self.id = id.lower()
        self.url = url.lower()
        self.title = title.lower()
        self.text = text.lower()

    def getID(self):
        return self.id

    def getURL(self):
        return self.url

    def getTitle(self):
        return self.title

    def getText(self):
        return self.text
