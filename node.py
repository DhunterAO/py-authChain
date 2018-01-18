from flask import Flask, request, jsonify, render_template
from util import is_valid_ip
from account import Account
from blockchain import Blockchain
from authorization import Authorization
import requests
import json
import socket


class Node:
    def __init__(self, ip="127.0.0.1", port=9000, neighbor_list=set(),
                 account=Account(), blockchain=Blockchain(), authorization_pool=set()):
        self._ip = ip
        self._port = port
        self._neighborList = neighbor_list
        self._account = account
        self._blockchain = blockchain
        self._authorizationPool = authorization_pool
        self.app = Flask(__name__)

        @self.app.route('/')
        def hello_world():
            return render_template('form.html')

        @self.app.route('/', methods=['POST'])
        def my_form_post():
            text = request.form['text']
            print(type(text))
            processed_text = text.upper()
            return processed_text

        @self.app.route('/mine', methods=['GET'])
        def mine():
            new_block = node.new_block()
            response = new_block.to_json()
            return jsonify(response), 200

        @self.app.route('/authorization/pool', methods=['GET'])
        def list_authorizations():
            response = node.get_authorization_pool()
            return jsonify(response), 200

        @self.app.route('/authorization/new', methods=['POST'])
        def new_authorization():
            get_json = request.get_json()
            required = ['inputs', 'outputs', 'duration', 'timestamp']
            if not all(k in get_json for k in required):
                return 'Missing values', 400
            get_authorization = json.load(get_json)

            # Create a new Transaction
            authorization = Authorization(get_authorization['inputs'], get_authorization['outputs'],
                                          get_authorization['duration'], get_authorization['timestamp'])
            node.add_authorization(authorization)
            response = authorization.to_json()
            return jsonify(response), 201

        @self.app.route('/blockchain', methods=['GET'])
        def list_blockchain():
            response = node.get_blockchain().to_json()
            return jsonify(response), 200

        @self.app.route('/neighbor/add')
        def add_page():
            return render_template('form.html')

        @self.app.route('/neighbor/add', methods=['POST'])
        def add_neighbor():
            neighbor = request.form['text']
            print('add neighbor')
            print(neighbor)
            if neighbor is None:
                return "Error: Please supply a valid list of neighbors", 400
            add = node.add_neighbor(neighbor)
            if add:
                response = node.get_neighbors()
                return jsonify(list(response)), 201
            else:
                response = ['invalid address, it should be like x.x.x.x:port']
                return jsonify(list(response)), 201

        @self.app.route('/neighbor/list', methods=['GET'])
        def list_neighbors():
            neighbors = node.get_neighbors()
            response = {
                'neighbors': list(neighbors)
            }
            return jsonify(response), 200

    def start(self, port):
        self.app.run(host='127.0.0.1', port=port)
        return

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
        if len(address.split(':')) != 2:
            return False
        ip = address.split(':')[0]
        port = address.split(':')[1]
        if is_valid_ip(ip) and port.isdigit():
            self._neighborList.add(address)
            return True
        return False

    def add_authorization(self, authorization):
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
        print(0)
        new_block = self._blockchain.generate_new_block(self._authorizationPool)
        print(1)
        self.broad_block(new_block)
        print(2)
        return new_block

    def get_blockchain(self):
        return self._blockchain

    def get_neighbors(self):
        return self._neighborList

    def get_authorization_pool(self):
        return self._authorizationPool


if __name__ == '__main__':
    node = Node()
    node.start(9000)
