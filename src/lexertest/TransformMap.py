class TransformMap:
    def __init__(self, rec, now, next_):
        self.rec = rec
        self.now = now
        self.next = next_

    def __lt__(self, other):
        return self.now + 100 * ord(self.rec) < other.now + 100 * ord(self.rec)