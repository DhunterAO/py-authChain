from flask import Flask, request, jsonify, render_template
from util import is_valid_ip, verify_signature
from account import Account
from blockchain import Blockchain
from duration import Duration
from limit import Limit
from input import Input
from output import Output
from dataURL import DataURL
from constant import MAX_DATA_RANGE
from authorization import Authorization
import requests
import hashlib
import json
import time
import os


class Node:
    def __init__(self, ip="127.0.0.1", port=9000, neighbor_list=[],
                 account=Account(), blockchain=Blockchain(), authorization_pool=[]
                 , data_path='./database'):
        self._ip = ip
        self._port = port
        self._neighborList = neighbor_list
        self._account = account
        self._blockchain = blockchain
        self._authorizationPool = authorization_pool
        self._database = []
        self._dataPath = data_path
        self.app = Flask(__name__)

        """
        @self.app.route('/')
        def hello_world():
            return render_template('entry.html')

        @self.app.route('/', methods=['POST'])
        def my_form_post():
            text = request.form['text']
            print(type(text))
            processed_text = text.upper()
            return processed_text
        """

        @self.app.route('/neighbor/add')
        def submit_neighbor():
            return render_template('submit_neighbor.html')

        @self.app.route('/neighbor/add', methods=['POST'])
        def add_neighbor():
            neighbors = request.form['text']
            print('add neighbors')
            print(neighbors)
            neighbors = json.loads(neighbors)
            if neighbors is None:
                return "Error: Please supply a valid list of neighbors", 400
            response = []
            for neighbor in neighbors:
                if not node.add_neighbor(neighbor):
                    info = neighbor + ' is invalid address, address should be like x.x.x.x:port'
                    response.append(info)
            response += list(node.get_neighbors())
            return jsonify(list(response)), 201

        @self.app.route('/neighbor/list', methods=['GET'])
        def list_neighbors():
            neighbors = node.get_neighbors()
            response = {
                'neighbors': list(neighbors)
            }
            return jsonify(response), 200

        @self.app.route('/blockchain', methods=['GET'])
        def list_blockchain():
            response = self.get_blockchain().to_json()
            return jsonify(response), 200

        @self.app.route('/authorization/pool', methods=['GET'])
        def list_authorizations():
            response = self.get_authorization_pool()
            return jsonify(list(response)), 200

        @self.app.route('/authorization/add', methods=['POST'])
        def add_authorization():
            get_json = json.loads(request)
            required = ['inputs', 'outputs', 'duration', 'timestamp']
            if not all(k in get_json for k in required):
                return 'Missing values', 400

            # Create a new Transaction
            authorization = Authorization(get_json['inputs'], get_json['outputs'],
                                          get_json['duration'], get_json['timestamp'])
            node.add_authorization(authorization)
            response = authorization.to_json()
            return jsonify(response), 201

        @self.app.route('/authorization/receive', methods=['POST'])
        def receive_authorization():
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

        @self.app.route('/mine', methods=['GET'])
        def mine():
            new_block = self.new_block()
            response = new_block.to_json()
            return jsonify(response), 200

        @self.app.route('/block/add')
        def submit_block():
            return render_template('submit_block.html')

        @self.app.route('/block/add', methods=['POST'])
        def add_block():
            get_json = request.form['text']
            return get_json

        @self.app.route('/block/receive', methods=['POST'])
        def receive_block():
            return render_template('submit_block.html')

        # some functions to solve data
        @self.app.route('/data/upload', methods=['POST'])
        def upload_data():
            # check if got enough values
            get_json = request.get_json()
            print(get_json)
            print(type(get_json))
            required = ['public_key', 'data', 'timestamp', 'op', 'signature']
            if not all(k in get_json for k in required):
                return 'Missing values', 400
            public_key = get_json['public_key']
            data = get_json['data']
            timestamp = get_json['timestamp']
            op = get_json['op']
            hash = hashlib.sha256((str(data) + str(timestamp) + str(0)).encode()).hexdigest()
            signature = get_json['signature']

            # check if op is upload operation
            if op != 0:
                return 'op is not matched!', 400

            # check if there is enough room
            if len(self._database) + len(get_json['data']) >= MAX_DATA_RANGE:
                return 'no enough storage', 400

            # check if timestamp is not expired
            if timestamp + 600 < time.time():
                return 'Request expired', 400

            # check if signature is matched
            print(signature)
            print(type(signature))

            if not verify_signature(public_key, hash, eval(signature)):
                return 'Signature unmatched', 400

            # everything is fine then store data into database
            if type(data) is 'list':
                self._database += data
            else:
                self._database.append(data)

            # generate a new authorization
            input = Input(0, 0, 0)

            if type(data) is 'list':
                data_url = DataURL(len(self._database) - len(data), len(self._database))
            else:
                data_url = DataURL(len(self._database) - 1, len(self._database))
            output = Output(recipient=public_key, data_url=data_url, limit=Limit(7))

            authorization = Authorization(inputs=[input], outputs=[output], duration=Duration(), timestamp=time.time())

            # sign this authorization
            input.add_signature(self._account.sign_message(authorization.calc_hash()))

            # store this authorization and broadcast it
            auth_number = self.add_authorization(authorization)
            print(auth_number)
            # return the position of authorization to client
            response = {
                'block_number': self._blockchain.get_height(),
                'auth_number': auth_number,
                'output_number': 0
            }
            return jsonify(response), 201

        # receive delete request
        @self.app.route('/data/delete', methods=['POST'])
        def delete_data():
            # check if got enough values
            get_json = request.get_json()
            required = ['public_key', 'data_url', 'timestamp', 'output_position', 'op', 'signature']
            if not all(k in get_json for k in required):
                return 'Missing values', 400
            public_key = get_json['public_key']
            data_url = get_json['data_url']
            timestamp = get_json['timestamp']
            output_position = get_json['output_position']
            op = get_json['op']
            hash = hashlib.sha256((str(data_url) + str(timestamp) + str(output_position) + str(1)).encode()).hexdigest()
            signature = get_json['signature']

            # check if op is delete operation
            if op != 1:
                return 'op is not matched!', 400

            # get output from the output_position and check the limit and data_url
            output = self._blockchain.get_output(output_position['block_number'],
                                                 output_position['authorization_number'],
                                                 output_position['output_number'])
            if not output.valid_limit(4):
                return 'error: limit out of range', 400
            if not output.valid_data_url(data_url.get_start(), data_url.get_end()):
                return 'error: data_url out of range', 400

            # check if timestamp is not expired
            if timestamp + 600 < time.time():
                return 'Request expired', 400

            # check if signature is matched
            if not verify_signature(public_key, hash, signature):
                return 'Signature unmatched', 400

            # if everything is fine then delete the data in data_url
            start = data_url['start']
            end = data_url['end']
            for i in range(start, end):
                self._database[i] = 0

            # return the delete information to client
            return 'delete successfully!', 201

        @self.app.route('/data/update', methods=['POST'])
        def update_data():
            # check if got enough values
            get_json = request.get_json()
            required = ['public_key', 'data', 'data_url', 'timestamp', 'output_position', 'op', 'signature']
            if not all(k in get_json for k in required):
                return 'Missing values', 400
            public_key = get_json['public_key']
            data = get_json['data']
            data_url = get_json['data_url']
            timestamp = get_json['timestamp']
            output_position = get_json['output_position']
            op = get_json['op']
            hash = hashlib.sha256((str(data_url) + str(timestamp) + str(output_position) + str(1)).encode()).hexdigest()
            signature = get_json['signature']

            # check if op is update operation
            if op != 2:
                return 'op is not matched!', 400

            # get output from the output_position and check the limit and data_url
            output = self._blockchain.get_output(output_position['block_number'],
                                                 output_position['authorization_number'],
                                                 output_position['output_number'])
            if not output.valid_limit(4):
                return 'error: limit out of range', 400
            if not output.valid_data_url(data_url.get_start(), data_url.get_end()):
                return 'error: data_url out of range', 400

            # check if timestamp is not expired
            if timestamp + 600 < time.time():
                return 'Request expired', 400

            # check if signature is matched
            if not verify_signature(public_key, hash, signature):
                return 'Signature unmatched', 400

            # check if there is enough room
            start = data_url['start']
            end = data_url['end']

            if isinstance(data, list) and len(data) > start - end:
                return 'no enough storage', 400

            # if everything is fine then update the data in data_url
            if isinstance(data, list):
                for i in range(start, start+len(data)):
                    self._database[i] = data[i-len(data)]
                for i in range(start+len(data), end):
                    self._database[i] = 0
            else:
                self._database[start] = data
                for i in range(start+1, end):
                    self._database[i] = 0

            # return the update information to client
            return 'update successfully!', 201

        @self.app.route('/data/read', methods=['POST'])
        def read_data():
            # check if got enough values
            get_json = request.get_json()
            required = ['public_key', 'data_url', 'timestamp', 'output_position', 'op', 'signature']
            if not all(k in get_json for k in required):
                return 'Missing values', 400
            public_key = get_json['public_key']
            data_url = get_json['data_url']
            timestamp = get_json['timestamp']
            output_position = get_json['output_position']
            op = get_json['op']
            hash = hashlib.sha256((str(data_url) + str(timestamp) + str(output_position) + str(1)).encode()).hexdigest()
            signature = get_json['signature']

            # check if op is read operation
            if op != 3:
                return 'op is not matched!', 400

            # get output from the output_position and check the limit and dataurl
            output = self._blockchain.get_output(output_position['block_number'],
                                                 output_position['authorization_number'],
                                                 output_position['output_number'])
            if not output.valid_limit(4):
                return 'error: limit out of range', 400
            if not output.valid_dataURL(get_json['data_url']):
                return 'error: data_url out of range', 400

            # check if timestamp is not expired
            if timestamp + 600 < time.time():
                return 'Request expired', 400

            # check if signature is matched
            if not verify_signature(public_key, hash, signature):
                return 'Signature unmatched', 400

            # if everything is fine then return the data in data_url
            start = data_url['start']
            end = data_url['end']
            return self._database[start:end], 201

        @self.app.route('/outputs/update', methods=['POST'])
        def update_outputs():
            # check if got enough values
            get_json = request.get_json()
            required = ['public_key', 'data_url', 'timestamp', 'output_position', 'op', 'signature']
            if not all(k in get_json for k in required):
                return 'Missing values', 400

            return

    def start(self):
        self.app.run(host='127.0.0.1', port=self._port)
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

    def add_address(self, address):
        self._account.add_address(address)
        return

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
            return -1
        self._authorizationPool.append(authorization)
        self.broad_authorization(authorization)
        return len(self._authorizationPool) - 1

    def broad_authorization(self, authorization, banned=None):
        for neighbor in self._neighborList:
            if neighbor != banned:
                requests.post(f'http://{neighbor}/receive_authorization', authorization)
        return

    def receive_authorization(self, authorization, source):
        if authorization in self._authorizationPool or not authorization.valid(self._blockchain):
            return
        self._authorizationPool.append(authorization)
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
            response = requests.get(f'http://{neighbor}/blockchain')
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
                requests.post(f'http://{neighbor}/block/receive', block)
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
        # print(0)
        new_block = self._blockchain.generate_new_block(self._authorizationPool)
        # print(1)
        self.broad_block(new_block)
        # print(2)
        return new_block

    def get_blockchain(self):
        return self._blockchain

    def get_neighbors(self):
        return self._neighborList

    def get_authorization_pool(self):
        return self._authorizationPool

    def to_json(self):
        node_json = {
            'ip': self._ip,
            'port': self._port,
            'neighborList': self._neighborList,
            'blockchain': self._blockchain.to_json(),
            'authorizationPool': [],
            'database': self._database
        }
        for auth in self._authorizationPool:
            node_json['authorizationPool'].append(auth.to_json())
        return node_json

    def store_node(self, file='node.txt'):
        node_path = os.path.join(self._dataPath, file)
        with open(node_path, 'w') as f:
            f.write(json.dumps(self.to_json()))
        return

    def load_node(self, file='node.txt'):
        node_path = os.path.join(self._dataPath, file)
        with open(node_path, 'r') as f:
            text = f.read()
        #print(account)
        self._ip = json.loads(text)["ip"]
        self._port = json.loads(text)["port"]
        self._neighborList = json.loads(text)["neighborList"]


        # print(account)
        # print(type(json.loads(account)))
        return


if __name__ == '__main__':
    node = Node(port=9000)
    node.start()
    node.store_node()
    node.load_node()

