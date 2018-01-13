import time
import hashlib

class Authorization:
    def __init__(self, inputs, outputs, duration=10):
        self.inputs = inputs
        self.outputs = outputs
        self.duration = duration
        self.timestamp = time.time()

    def addInput(self, input):
        self.inputs.append(input)

    def removeInput(self, input):
        self.inputs.remove(input)

    def addOutput(self, output):
        self.outputs.append(output)

    def removeOutput(self, output):
        self.outputs.remove(output)

    def setDuration(self, duration):
        self.duration = duration

    def __str__(self):
        m = ""
        for i in self.inputs:
            m += str(i)

        for i in self.outputs:
            m += str(i)

        m += str(self.timestamp)
        m += str(self.duration)

        return m

    def calcHash(self):
        return hashlib.sha256(str(self).encode('utf-8')).hexdigest()
