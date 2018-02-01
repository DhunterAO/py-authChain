class Limit:

    def __init__(self, limit=0):
        self._limit = limit
        return

    def set(self, limit):
        self._limit = limit
        return

    def add_read(self):
        self._limit |= 1
        return

    def remove_read(self):
        self._limit &= ~1
        return

    def add_append(self):
        self._limit |= 2
        return

    def remove_append(self):
        self._limit &= ~2
        return

    def add_delete(self):
        self._limit |= 4
        return

    def valid(self, given_limit):
        return (self._limit & given_limit) == self._limit

    def value(self):
        return self._limit

    def __str__(self):
        return str(self._limit)


if __name__ == '__main__':
    l = Limit()
    print(str(l))
    l.add_append()
    print(str(l))
    l.add_read()

    print(str(l))
    print(l.valid(3))
    print(l.valid(4))

