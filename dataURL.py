import logging


class DataURL:
    def __init__(self, start=0, end=0):
        if start <= end:
            self._start = start
            self._end = end
        else:
            self._start = 0
            self._end = 0
            logging.warning("start should be less or equal than end")
        return

    def set(self, start, end):
        if start <= end:
            self._start = start
            self._end = end
        else:
            logging.warning("start should be less or equal than end")
        return

    def set_start(self, start):
        if start <= self._end:
            self._start = start
        else:
            logging.warning("start should be less or equal than end")
        return

    def get_start(self):
        return self._start

    def set_end(self, end):
        if end >= self._start:
            self._end = end
        else:
            logging.warning("start should be less or equal than end")
        return

    def get_end(self):
        return self._end

    def contains(self, given_start, given_end):
        return self._start <= given_start < given_end <= self._end

    def belongs(self, given_start, given_end):
        return given_start <= self._start < self._end <= given_end

    def to_json(self):
        json = {
            'start': self._start,
            'end': self._end
        }
        return json

    def from_json(self, json):
        required = ['start', 'end']
        if not all(k in json for k in required):
            logging.warning(f"value missing in {required}")
            return False

        if not isinstance(json['start'], int) or not isinstance(json['end'], int) or json['start']>json['end']:
            logging.warning("start and end should be both type<int> and start should be less or equal than end")
            return False

        self._start = json['start']
        self._end = json['end']
        return True

    def __str__(self):
        return str(self._start) + str(self._end)


if __name__ == '__main__':
    d = DataURL(10, 12)
    print(str(d))
    d.set(11, 3)
    print(str(d))
    d.set_start(2)
    print(str(d))
    d.set_end(10)
    print(str(d))

