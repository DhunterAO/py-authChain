from ecdsa import VerifyingKey


class Input:

    def __init__(self, block_number=-1, auth_number=-1, output_number=-1, signature=None):
        self._blockNumber = block_number
        self._authNumber = auth_number
        self._outputNumber = output_number
        self._signature = signature

    def set_block_number(self, block_number):
        self._blockNumber = block_number

    def get_block_number(self):
        return self._blockNumber

    def set_auth_number(self, auth_number):
        self._authNumber = auth_number

    def get_auth_number(self):
        return self._authNumber

    def set_output_number(self, output_number):
        self._outputNumber = output_number

    def get_output_number(self):
        return self._outputNumber

    def add_signature(self, signature):
        self._signature = signature

    def valid(self, blockchain, message):
        source_out = blockchain.findOut(self._blockNumber, self._authNumber, self._outputNumber)
        source_pubkey = source_out.getAddress()
        source_pubkey = VerifyingKey.from_string(source_pubkey)
        return source_pubkey.verify(self._signature, message.encode("utf-8"))

    def __str__(self):
        return str(self._blockNumber)+str(self._authNumber)+str(self._outputNumber)


if __name__ == '__main__':
    input = Input(10, 12, 3)
    print(str(input))
    input.add_signature("signature")
    print(str(input))
