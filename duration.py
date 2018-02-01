import time
import logging


class Duration:
    def __init__(self, end=0, start=0):
        self._start = start
        self._end = end

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end

    def set(self, end, start=0):
        self._start = start
        self._end = end

    def valid(self, block_number):
        if self._end == 0:
            return True
        if self._end > 1000000000:
            return self._start <= time.time() <= self._end
        return self._start <= block_number <= self._end

    def to_json(self):
        json = {
            'start_time': self._start,
            'end_time': self._end
        }
        return json

    def from_json(self, json):
        required = ['start_time', 'end_time']
        if not all(k in json for k in required):
            logging.warning(f"value missing in {required}")
            return False

        if not isinstance(json['start_time'], (int, float)) or not isinstance(json['end_time'], (int, float)) \
           or not type(json['start_time']) == type(json['end_time']):
            logging.warning("start_time and end_time should be both type<int> or type<float>")
            return False

        self._start = json['start_time']
        self._end = json['end_time']
        return True

    def __str__(self):
        return str(self._start)+str(self._end)


if __name__ == '__main__':
    d = Duration(1000)
    print(str(d))
    d.set(10000000000000000, 20)
    d.from_json([])
    print(str(d))
    print(d.valid(110))
    print(time.time())

