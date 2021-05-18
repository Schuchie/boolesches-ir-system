import tokenizer


class Document:
    def __init__(self, id, url, title, text):
        self.id = id.lower()
        self.url = url.lower()
        self._title = title
        self.title = list(tokenizer.tokenize(title.lower()))
        self._text = text
        self.text = list(tokenizer.tokenize(text.lower()))

    def get_id(self):
        return self.id

    def get_url(self):
        return self.url

    def get_title(self):
        return self.title

    def get_text(self):
        return self.text

    def get_title2(self):
        return self.__title
