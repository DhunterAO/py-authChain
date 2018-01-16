from flask import Flask
from account import Account
from blockchain import Blockchain
from urllib.parse import urlparse
from argparse import ArgumentParser
import requests
import flask


class Node:
    def __init__(self, ip="127.0.0.1", port=9000, neighbor_list={'127.0.0.1:9000'},
                 account=Account(), blockchain=Blockchain(), authorization_pool = set()):
        self._ip = ip
        self._port = port
        self._neighborList = neighbor_list
        self._account = account
        self._blockchain = blockchain
        self._authorizationPool = authorization_pool

    def set_ip(self, ip: str):
        self._ip = ip
        return

    def get_ip(self):
        return self._ip

    def set_port(self, port):
        self._port = port
        return

    def get_port(self):
        return self._port

    def add_neighbor(self, address):
        parsed_url = urlparse(address)
        self._neighborList.add(parsed_url.netloc)
        return

    def new_authorization(self, authorization):
        if authorization in self._authorizationPool or not authorization.valid(self._blockchain):
            return
        self._authorizationPool.add(authorization)
        self.broad_authorization(authorization)
        return

    def broad_authorization(self, authorization, banned=None):
        for neighbor in self._neighborList:
            if neighbor != banned:
                requests.post(f'http://{neighbor}/receive_authorization', authorization)
        return

    def receive_authorization(self, authorization, source):
        if authorization in self._authorizationPool or not authorization.valid(self._blockchain):
            return
        self._authorizationPool.add(authorization)
        self.broad_authorization(authorization, source)
        return

    def valid_blockchain(self, blockchain=None):
        if blockchain is None:
            return self._blockchain.valid()
        return blockchain.valid()

    def resolve_conflict(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.

        :return: True if our chain was replaced, False if not
        """
        new_chain = None
        max_length = len(self._blockchain)
        # Grab and verify the chains from all the nodes in our neighbors
        for neighbor in self._neighborList:
            response = requests.get(f'http://{neighbor}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_blockchain(chain):
                    max_length = length
                    new_chain = chain
        if new_chain is not None:
            self._blockchain = new_chain
            return True
        return False

    def broad_block(self, block, banned=None):
        for neighbor in self._neighborList:
            if neighbor != banned:
                requests.post(f'http://{neighbor}/receive_block', block)
        return

    def receive_block(self, block, source):
        """
        When receiving a new block from source, judging if it exists in self._blockchain.

        """
        if not block.valid():
            return
        if block.get_prev_hash() == self._blockchain[-1].get_now_hash():
            self._blockchain.add_new_block(block)
            self.broad_block(block, source)
            return
        if self._blockchain.contain(block.get_now_hash()):
            return
        if self.resolve_conflict():
            self.broad_block(block, source)
        return

    def new_block(self):
        """
        Create a new Block in the Blockchain

        :return: New Block
        """
        new_block = self._blockchain.generate_new_block(self._authorizationPool)
        self.broad_block(new_block)
        return new_block


app = Flask(__name__)
node = Node()


@app.route('/mine', methods=['GET'])
def mine():
    new_block = node.new_block()
    return new_block.tojson(), 200



def main(port):
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    main(port)


