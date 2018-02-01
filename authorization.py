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

    def to_json(self):
        inputs_json = []
        for input in self._inputs:
            inputs_json.append(input.to_json())
        outputs_json = []
        for output in self._outputs:
            outputs_json.append(output.to_json())
        json = {
            'inputs': inputs_json,
            'outputs': outputs_json,
            'duration': self._duration.to_json(),
            'timestamp': self._timestamp
        }
        return json

    def valid(self, blockchain):
        hash = self.calc_hash()
        givens = []
        for input in self._inputs:
            if not input.valid(blockchain, hash):
                print('input invalid')
                return False
            out = blockchain.get_output(input.get_block_number(), input.get_auth_number(), input.get_output_number())
            givens.append((out.get_data_url().get_start(), out.get_data_url().get_end(), out.get_limit().value()))

        for output in self._outputs:
            if not output.valid(givens):
                print('output invalid')
                return False

        if not self._duration.valid(blockchain.get_height()):
            print('duration invalid')
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

