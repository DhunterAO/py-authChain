
class Input:

    def __init__(self, prevAuHash, prevIndex):
        self.prevAuHash = prevAuHash
        self.prevIndex  = prevIndex

    def add_signature(self, signature):
        self.signature = signature

    def __str__(self):
        return str(self.prevAuHash)+str(self.prevIndex)