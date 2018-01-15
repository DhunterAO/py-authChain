from block import Block


class Blockchain:
    def __init__(self, difficult=int("0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",16)):
        self._blockchain = []
        self._difficult = difficult

    def get_block(self, block_number):
        return self._blockchain[block_number]

    def get_authorization(self, block_number, authorization_number):
        return self.get_block(block_number).get_authorization(authorization_number)

    def get_output(self, block_number, authorization_number, output_number):
        return self._blockchain[block_number].getAutherization(authorization_number).getOut(output_number)

    def generate_new_block(self):
        new_block = Block(self._blockchain[-1].get_now_hash())
        self._blockchain.append(new_block)

        if len(self._blockchain) % 100 == 1:
            self._difficult *= 6000/(self._blockchain[-1].get_timestamp()-self._blockchain[-101].get_timestamp())
        new_hash = new_block.calc_hash()
        while int(new_hash, 16) > self._difficult:
            new_block.update()
        return new_block

