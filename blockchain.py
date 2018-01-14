
class Blockchain:

    def __init__(self):
        self._blockchain = []

    def findOut(self, block_number, auth_number, out_number):
        return self._blockchain[block_number].getAuth(auth_number).getOut(out_number)