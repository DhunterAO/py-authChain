from block import Block
import logging
import constant
from constant import GENESIS_BLOCK


class Blockchain:
    def __init__(self, genesis_block=GENESIS_BLOCK, blockchain=None,
                 difficulty="0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"):
        if blockchain is None:
            self._blockchain = []
            self._blockchain.append(genesis_block)
        else:
            self._blockchain = blockchain
            if self._blockchain[0] is not genesis_block:
                logging.error("genesis_block is not the head of the blockchain")
                return
        self._difficulty = difficulty

    def get_height(self):
        return len(self._blockchain)

    def get_block(self, block_number):
        return self._blockchain[block_number]

    def get_authorization(self, block_number, authorization_number):
        return self.get_block(block_number).get_authorization(authorization_number)

    def get_output(self, block_number, authorization_number, output_number):
        try:
            output = self._blockchain[block_number].get_authorization(authorization_number).get_output(output_number)
        except IndexError:
            logging.error("index out of range")
            return None
        else:
            return output

    def add_new_block(self, block):
        if block.get_prev_hash() == self._blockchain[-1].get_now_hash():
            self._blockchain.append(block)
        else:
            logging.error("the new block does not match the blockchain")
        return

    def generate_new_block(self, authorizations):
        new_block = Block(self._blockchain[-1].get_now_hash(), authorizations)
        while new_block.calc_hash() > self._difficulty:
            new_block.update()
        self._blockchain.append(new_block)
        return new_block

    def valid(self):
        if self._blockchain[0] != GENESIS_BLOCK:
            logging.warning('the head of blockchain should be GENESIS_BLOCK')
            return False
        for i in range(1, len(self._blockchain)):
            if self._blockchain[i].get_prev_hash() != self._blockchain[i-1].get_now_hash():
                logging.warning(f'the {i}th block does not match the previous one')
                return False
            if not self._blockchain[i].valid(self) or self._blockchain[i].get_now_hash() > self._difficulty:
                logging.warning(f'the {i}th block is invalid')
                return False
        return True

    def contain(self, hash):
        for block in self._blockchain:
            if block.get_now_hash() == hash:
                return True
        return False

    def to_json(self):
        json = {
            'height': len(self._blockchain),
            'difficulty': self._difficulty,
            'blockchain': []
        }
        for block in self._blockchain:
            json['blockchain'].append(block.to_json())
        return json

    def from_json(self, json):
        required = ['height', 'difficulty', 'blockchain']
        if not all(k in json for k in required):
            logging.warning(f'value missing in {required}')
            return False

        if not isinstance(json['height'], int) or not isinstance(json['difficulty'], str) \
                or not isinstance(json['blockchain'], list):
            logging.warning("height should be both type<int>, difficulty should be type<str> "
                            "and blockchain should be type<list>")
            return False

        self._difficulty = json['difficulty']
        chain = []
        for block in json['blockchain']:
            b = Block()
            if not b.from_json(block):
                return False
            chain.append(b)
        self._blockchain = chain
        return True


if __name__ == '__main__':
    my_chain = Blockchain()
    gen_block = my_chain.get_block(0)
    print(my_chain.valid())
    my_chain.generate_new_block([])
    print(my_chain.to_json())
    print(my_chain.valid())

    y = Blockchain()
    print(y.from_json(my_chain.to_json()))
    print(y.to_json())
