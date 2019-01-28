class Builder:
    def __init__(self, vocab: str = None):
        self.vocab = vocab
        self.next = None
        self.prev = None

        words = [w for w in open("vocab/" + self.vocab.lower() + ".voc").read().split('\n') if w != '']
        self.check = lambda string: any(w in string for w in words)
        self.len = 1

    def require(self, vocab):
        next = Builder(vocab)
        self.next = next
        next.prev = self
        self.len += 1
        return next

    def match(self, string: str) -> bool:
        current = self
        while current is not None:
            matched = current.check(string)
            if not matched:
                return False
            current = current.prev
        return True


class IntentBuilder:
    def __init__(self, builder: Builder):
        self.builder = builder

    def __call__(self, func):
        def wrapper(string: str):
            if not self.builder.match(string.lower()):
                return False
            return func(string.lower())
        return wrapper

