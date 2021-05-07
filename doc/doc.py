import tokenizer


class Document:
    def __init__(self, id, url, title, text):
        self.id = id.lower()
        self.url = url.lower()
        self.title = list(tokenizer.tokenize(title.lower()))
        self.text = list(tokenizer.tokenize(text.lower()))

    def get_id(self):
        return self.id

    def get_url(self):
        return self.url

    def get_title(self):
        return self.title

    def get_text(self):
        return self.text
