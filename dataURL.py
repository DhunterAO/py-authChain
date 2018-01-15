
class DataURL:

    def __init__(self, location=0, length=0):
        self._location = location
        self._length = length

    def set(self, location, length):
        self._location = location
        self._length = length

    def set_location(self, location):
        self._location = location

    def get_location(self):
        return self._location

    def set_length(self, length):
        self._length = length

    def get_length(self):
        return self._length

    def __str__(self):
        return str(self._location) + str(self._length)


if __name__ == '__main__':
    d = DataURL(10, 2)
    print(str(d))
    d.set(11, 3)
    print(str(d))
    d.set_location(2)
    print(str(d))
    d.set_length(10)
    print(str(d))

