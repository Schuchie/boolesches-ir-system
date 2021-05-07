class Document:
    def __init__(self, id, url, title, text):
        self.id = id.lower()
        self.url = url.lower()
        self.title = title.lower()
        self.text = text.lower()

    def get_id(self):
        return self.id

    def get_url(self):
        return self.url

    def get_title(self):
        return self.title

    def get_text(self):
        return self.text
