

class Output:

    def __init__(self, recipient, dataURL, limit):
        self.recipient = recipient
        self.dataURL = dataURL
        self.limit = limit

    def __str__(self):
        return str(self.recipient) + str(self.dataURL) + str(self.limit)