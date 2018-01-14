import time


class Duration:
    def __init__(self, end=0, start=0):
        self._start = start
        self._end = end

    def set(self, end, start=0):
        self._start = start
        self._end = end

    def valid(self, block_number):
        if self._end == 0:
            return True
        if self._start > 1000000000:
            return self._start <= time.time() <= self._end
        return self._start <= block_number <= self._end
