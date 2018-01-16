from block import Block
import logging


class Blockchain:
    def __init__(self, genesis_block, blockchain=None,
                 difficulty=int("0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",16)):
        if blockchain is None:
            self._blockchain = []
            self._blockchain[0] = genesis_block
        else:
            self._blockchain = blockchain
            if self._blockchain[0] is not genesis_block:
                logging.error("genesis_block is not the head of the blockchain")
                return
        self._difficulty = difficulty

    def get_block(self, block_number):
        return self._blockchain[block_number]

    def get_authorization(self, block_number, authorization_number):
        return self.get_block(block_number).get_authorization(authorization_number)

    def get_output(self, block_number, authorization_number, output_number):
        return self._blockchain[block_number].get_autherization(authorization_number).get_output(output_number)

    def add_new_block(self, block):
        if block.get_prev_hash() == self._blockchain[-1].get_now_hash():
            self._blockchain.append(block)
        else:
            logging.error("the new block does not match the blockchain")
        return

    def generate_new_block(self, authorizations):
        new_block = Block(self._blockchain[-1].get_now_hash(), authorizations)
        self._blockchain.append(new_block)
        if len(self._blockchain) % 100 == 1:
            self._difficulty *= 6000/(self._blockchain[-1].get_timestamp()-self._blockchain[-101].get_timestamp())

        new_hash = new_block.calc_hash()
        while int(new_hash, 16) > self._difficulty:
            new_block.update()
        return new_block

    def valid(self):
        if not self._blockchain[0].valid(self):
            return False
        for i in range(1,len(self._blockchain)):
            if self._blockchain[i].get_prev_hash != self._blockchain[i-1].get_now_hash:
                return False
            if not self._blockchain[1].valid(self):
                return False
        return True

    def contain(self, hash):
        for block in self._blockchain:
            if block.get_now_hash() == hash:
                return True
        return False


if __name__ == '__main__':
    blockchain = Blockchain()