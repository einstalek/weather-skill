class Builder:
    def __init__(self, vocab: str = None):
        self.vocab = vocab
        self.next = None
        self.prev = None


        words = [w for w in open("vocab/" + self.vocab + ".voc").read().split('\n') if w != '']
        self.check = lambda string: any(w in string for w in words)

    def require(self, vocab):
        next = Builder(vocab)
        self.next = next
        next.prev = self
        return next

    def match(self, string: str) -> bool:
        current = self
        while current is not None:
            matched = current.check(string)
            if not matched:
                return False
            current = current.prev
        return True

    def __str__(self):
        current = self
        res = ""
        while current is not None:
            res += " " + current.vocab
            current = current.prev
        return res


if __name__ == "__main__":
    builder = Builder("forecast").require("weather").require("temp")
    print(builder)
