from ecdsa import VerifyingKey
from blockchain import findOut


class Input:

    def __init__(self, block_number, auth_number, output_number, signature=None):
        self._blockNumber = block_number
        self._authNumber = auth_number
        self._outputNumber = output_number
        self._signature = signature

    def add_signature(self, signature):
        self._signature = signature

    def valid(self, message):
        source_out = findOut(self._blockNumber, self._authNumber, self._outputNumber)
        source_pubkey = source_out.getOut()
        source_pubkey = VerifyingKey.from_string(source_pubkey)
        return source_pubkey.verify(self._signature, message.encode("utf-8"))

    def __str__(self):
        return str(self.prevAuHash)+str(self.prevIndex)