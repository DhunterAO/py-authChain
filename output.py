from dataURL import DataURL


class Output:
    def __init__(self, recipient=None, data_url=None, limit=None):
        self._recipient = recipient
        self._dataURL = data_url
        self._limit = limit
        return

    def set_recipient(self, recipient):
        self._recipient = recipient
        return

    def get_recipient(self):
        return self._recipient

    def set_data_url(self, data_url):
        self._dataURL = data_url

    def get_data_url(self):
        return self._dataURL

    def set_limit(self, limit):
        self._limit = limit
        return

    def get_limit(self):
        return self._limit

    def valid(self, givens):
        for given in givens:
            if self._dataURL.valid(given[0],given[1]) and self._limit.valid(given[2]):
                return True
        return False

    def __str__(self):
        return str(self._recipient) + str(self._dataURL) + str(self._limit)


if __name__ == '__main__':
    output = Output()
    output.set_recipient("aaxxbb")
    output.set_data_url(DataURL(10, 3))
    print(str(output))
    output.set_limit(2)
    print(str(output))
