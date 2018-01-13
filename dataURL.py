
class DataURL:

    def __init__(self, location=0, length=0):
        self.location = location
        self.length   = length

    def set(self, location, length):
        self.location = location
        self.length   = length

    def __str__(self):
        return str(self.location) + str(self.length)
