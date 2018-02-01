from dataURL import DataURL
from limit import Limit
import logging


class Output:
    def __init__(self, recipient=None, start=None, end=None, limit=None):
        if recipient is None:
            self._recipient = ''
        else:
            self._recipient = recipient

        if start is None or end is None:
            self._dataURL = DataURL()
        else:
            self._dataURL = DataURL(start, end)

        if limit is None:
            self._limit = Limit()
        else:
            self._limit = Limit(limit)
        return

    def set_recipient(self, recipient):
        self._recipient = recipient
        return

    def get_recipient(self):
        return self._recipient

    def set_data_url(self, data_url):
        self._dataURL = data_url
        return

    def get_data_url(self):
        return self._dataURL

    def data_url_contains(self, start, end):
        return self._dataURL.contains(start, end)

    def data_url_belongs(self, start, end):
        return self._dataURL.belongs(start, end)

    def set_limit(self, limit):
        self._limit.set(limit)
        return

    def get_limit(self):
        return self._limit

    def valid_limit(self, limit):
        return self._limit.valid(limit)

    def valid(self, givens):
        # print(givens)
        for given in givens:
            if self.data_url_belongs(given[0], given[1]) and self.valid_limit(given[2]):
                return True
        logging.warning('this output does not match any given data_url or limit')
        return False

    def to_json(self):
        json = {
            'recipient': self._recipient,
            'data_url': self._dataURL.to_json(),
            'limit': self._limit.value()
        }
        return json

    def from_json(self, json):
        required = ['recipient', 'data_url', 'limit']
        if not all(k in json for k in required):
            logging.warning(f"value missing in {required}")
            return False

        data_url = DataURL()
        if not data_url.from_json(json['data_url']):
            return False
        self._dataURL = data_url

        if not isinstance(json['recipient'], str) or not isinstance(json['limit'], int):
            logging.warning("recipient should be all type<str> and limit should be type<int>")
            return False

        self._recipient = json['recipient']
        self._limit = Limit(json['limit'])
        return True

    def __str__(self):
        return str(self._recipient) + str(self._dataURL) + str(self._limit)


if __name__ == '__main__':
    output = Output()
    output.set_recipient("aaxxbb")
    output.set_data_url(DataURL(10, 3))
    print(str(output))
    output.set_limit(2)
    print(str(output))
    print(output.to_json())
    u = Output()
    print(u.from_json(output.to_json()))
    print(u.to_json())
