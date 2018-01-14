import time
import hashlib


class Authorization:
    def __init__(self, inputs, outputs, duration=None):
        self._inputs = inputs
        self._outputs = outputs
        self._duration = duration
        self._timestamp = time.time()

    def addInput(self, input):
        self._inputs.append(input)

    def removeInput(self, input):
        self._inputs.remove(input)

    def addOutput(self, output):
        self._outputs.append(output)

    def removeOutput(self, output):
        self._outputs.remove(output)

    def getOutput(self, index):
        return self._outputs[index]

    def setDuration(self, start, end):
        self._duration.set(start, end)

    def calcHash(self):
        return hashlib.sha256(str(self).encode('utf-8')).hexdigest()

    def valid(self):
        hash = self.calcHash()
        for input in self._inputs:
            if not input.valid(hash):
                return False
        return True

    def __str__(self):
        m = ""
        for i in self.inputs:
            m += str(i)

        for i in self.outputs:
            m += str(i)

        m += str(self.timestamp)
        m += str(self.duration)

        return m


if __name__ == '__main__':
    print(time.time())