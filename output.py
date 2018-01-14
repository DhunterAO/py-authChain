

class Output:
    def __init__(self, recipient, dataURL, limit):
        self._recipient = recipient
        self._dataURL = dataURL
        self._limit = limit

    def getOut(self):
        return self._recipient

    def __str__(self):
        return str(self._recipient) + str(self._dataURL) + str(self._limit)