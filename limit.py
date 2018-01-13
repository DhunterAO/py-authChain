
class Limit:

    def __init__(self, limit=0):
        self.limit = limit

    def addRead(self):
        self.limit &= 1

    def addAppend(self):
        self.limit &= 2

    def addDelete(self):
        self.limit &= 4

    def __str__(self):
        return str(self.limit)
