import hashlib

from account import Account
from dataURL import DataURL

import hashlib
import requests
import logging
import json
import time
import os
from argparse import ArgumentParser

from output import Output


class Client:
    def __init__(self, account=Account(), data_path='./database', outputs=None):
        self._account = account
        self._path = data_path
        if outputs is None:
            self._outputs = set()
        else:
            self._outputs = outputs

    # some functions about account

    def create_address(self):
        self._account.create_address()
        return

    def load_account(self, file='account.txt'):
        account_path = os.path.join(self._path, file)
        with open(account_path, 'r') as f:
            account = f.read()
        # print(account)
        address_list = json.loads(account)["address_list"]
        for a in address_list:
            # print(a["private_key"])
            self._account.add_address_from_private_key(a["private_key"])

        # print(account)
        # print(type(json.loads(account)))
        return

    def store_account(self, file='account.txt'):
        account_path = os.path.join(self._path, file)
        with open(account_path, 'w') as f:
            f.write(json.dumps(self.to_json()))
        return

    # some functions about outputs

    def update_outputs(self, server_address, address_index=0):
        public_key = self._account.get_address(address_index).get_pubkey()
        now_time = time.time()
        hash = hashlib.sha256((str(now_time)).encode()).hexdigest()
        signature = self._account.sign_message(hash, address_index)
        send_json = {
            'public_key': public_key,
            'timestamp': now_time,
            'signature': signature
        }
        response = requests.post(f"http://{server_address}/outputs/update", json=send_json)

        if response.status_code == 200:
            return_json = response.json()['data_url']
            new_outputs = return_json['new_outputs']
            for out in new_outputs:
                self._outputs.add(out)
        else:
            logging.error('invalid response')
            return False

    # some option about data

    def upload_data(self, server_address, data, address_index=0):
        """
        Upload data to server and get back the dataURL

        :param server_address: x.x.x.x:port
        :param data: data you want to upload
        :param address_index: address index in address_list
        :return: dataURL where the data stores
        """
        public_key = self._account.get_address(address_index).get_pubkey()
        now_time = time.time()
        hash = hashlib.sha256((str(data)+str(now_time)).encode()).hexdigest()
        signature = self._account.sign_message(hash, address_index)
        send_json = {
            'public_key': public_key,
            'data': data,
            'timestamp': now_time,
            'signature': signature
        }
        response = requests.post(f"http://{server_address}/data/upload", json=send_json)

        if response.status_code == 200:
            return_json = response.json()['data_url']
            data_url = DataURL(return_json['start'], return_json['end'])
            out = Output(public_key, data_url, 7)
            self._outputs.add(out)
            return True
        else:
            logging.error('invalid response')
            return False

    def read_data(self, server_address, data_url, output, address_index=0):
        """

        :param server_address:
        :param data_url:
        :param output:
        :param address_index:
        :return:
        """
        public_key = self._account.get_address(address_index).get_pubkey()
        now_time = time.time()
        hash = hashlib.sha256((str(data_url)+str(now_time)+str(0)).encode()).hexdigest()
        signature = self._account.sign_message(hash, address_index)
        send_json = {
            'public_key': public_key,
            'data_url': data_url.to_json(),
            'output': output,
            'timestamp': now_time,
            'signature': signature,
            'op': 0
        }

        response = requests.post(f"http://{server_address}/data/read", json=send_json)
        if response.status_code == 200:
            return True
        else:
            logging.error('invalid response')
            return False

    def delete_data(self, server_address, data_url, address_index=0):
        """

        :param server_address:
        :param data_url:
        :param address_index:
        :return:
        """
        public_key = self._account.get_address(address_index).get_pubkey()
        now_time = time.time()
        hash = hashlib.sha256((str(data_url)+str(now_time)+str(1)).encode()).hexdigest()
        signature = self._account.sign_message(hash, address_index)
        send_json = {
            'public_key': public_key,
            'data_url': data_url.to_json(),
            'timestamp': now_time,
            'signature': signature,
            'op': 1
        }

        response = requests.post(f"http://{server_address}/data/delete", json=send_json)
        if response.status_code == 200:
            return True
        else:
            logging.error('invalid response')
            return False

    def update_data(self, server_address, data, data_url, address_index=0):
        """
        Upload data to server and get back the dataURL

        :param server_address: x.x.x.x:port
        :param data: data you want to update
        :param data_url: data position
        :param address_index: address index in address_list
        :return: dataURL where the data stores
        """
        public_key = self._account.get_address(address_index).get_pubkey()
        now_time = time.time()
        hash = hashlib.sha256((str(data)+str(data_url)+str(now_time)).encode()).hexdigest()
        signature = self._account.sign_message(hash, address_index)
        send_json = {
            'public_key': public_key,
            'data': data,
            'data_url': data_url,
            'timestamp': now_time,
            'signature': signature
        }
        response = requests.post(f"http://{server_address}/data/update", json=send_json)

        if response.status_code == 200:
            return True
        else:
            logging.error('invalid response')
            return False

    # some universal functions
    def to_json(self):
        # print(type(self._account.to_json()))
        return self._account.to_json()


if __name__ == '__main__':
    client = Client()
    # print(1)
    client.create_address()
    # print(2)
    # print(client.to_json())
    # print(3)
    client.store_account()
    # print(4)
    client.load_account()
    # print(5)
    # print(client.to_json())
