class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text

    def trim_left(self) -> None:
        i = 0
        while i < len(self.text) and self.text[i].isspace():
            i += 1

        self.text = self.text[i:]

    def chop_word(self):
        i = 0
        while i < len(self.text) and self.text[i].isalpha() or self.text[i] == "'":
            i += 1
        token = self.text[:i].upper()
        self.text = self.text[i:]
        return token

    def next_token(self):
        self.trim_left()

        if len(self.text) == 0:
            return None

        if self.text[0].isalpha():
            return self.chop_word()
        else:
            token = self.text[0]
            self.text = self.text[1:]
            return token
