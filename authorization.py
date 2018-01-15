import time
import hashlib
from duration import Duration
from input import Input
from output import Output


class Authorization:
    def __init__(self, inputs=[], outputs=[], duration=None, timestamp=None):
        self._inputs = inputs
        self._outputs = outputs
        if duration is None:
            self._duration = Duration()
        else:
            self._duration = duration

        if timestamp is None:
            self._timestamp = time.time()
        else:
            self._timestamp = timestamp

    def add_input(self, input):
        self._inputs.append(input)

    def remove_input(self, input):
        self._inputs.remove(input)

    def add_output(self, output):
        self._outputs.append(output)

    def remove_output(self, output):
        self._outputs.remove(output)

    def get_output(self, index):
        return self._outputs[index]

    def set_duration(self, end, start):
        self._duration.set(end, start)

    def calc_hash(self):
        return hashlib.sha256(str(self).encode('utf-8')).hexdigest()

    def valid(self):
        hash = self.calcHash()
        for input in self._inputs:
            if not input.valid(hash):
                return False
        return True

    def __str__(self):
        m = ""
        for i in self._inputs:
            m += str(i)

        for i in self._outputs:
            m += str(i)

        m += str(self._timestamp)
        m += str(self._duration)

        return m


if __name__ == '__main__':
    auth = Authorization()
    print(time.time())
    print(auth.calc_hash())
    a = auth.calc_hash()
    auth.set_duration(100, 20)
    print(str(auth))
    b = auth.calc_hash()
    print(auth.calc_hash())
    print(type(a))
    print(int(a,16))
    print(int("ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",16))
    print(a<"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
    auth.add_input(Input())
    auth.add_output(Output())

