from node import Node
from account import Account
import requests
import logging
import json
from argparse import ArgumentParser
import os


class Client:
    def __init__(self, account=Account(), data_path='./database', node=Node()):
        self._account = account
        self._path = data_path

    def create_address(self):
        self._account.create_address()
        return

    def to_json(self):
        #print(type(self._account.to_json()))
        return self._account.to_json()

    def load_account(self, file='account.txt'):
        account_path = os.path.join(self._path, file)
        with open(account_path, 'r') as f:
            account = f.read()
        #print(account)
        list = json.loads(account)["address_list"]
        for a in list:
            #print(a["private_key"])
            self._account.add_address_from_private_key(a["private_key"])

        #print(account)
        #print(type(json.loads(account)))
        return

    def store_account(self, file='account.txt'):
        account_path = os.path.join(self._path, file)
        with open(account_path, 'w') as f:
            f.write(json.dumps(self.to_json()))
        return

    def upload_data(self, server_address, data, address_index=0, data_url=None):
        """
        Upload data to server and get back the dataURL

        :param server_address: x.x.x.x:port
        :param data: data you want to upload
        :param address_index: address index in address_list
        :param data_url: if you know the data_url, then adjust it, or the server will create one and tell you data_url
        :return: dataURL where the data stores
        """
        signature = self._account.sign_message(str(data)+str(data_url), address_index)
        if data_url is not None:
            json = {
                'data': data,
                'data_url': data_url,
                'signature': signature
            }
        else:
            json = {
                'data': data,
                'signature': signature
            }
        response = requests.post(f"http://{server_address}/data/upload", json=json)
        return response

    def delete_data(self, server_address, data_url, address_index=0):
        """

        :param server_address:
        :param data_url:
        :param address_index:
        :return:
        """
        signature = self._account.sign_message(str(data_url), address_index)
        json = {
            'data_url': data_url,
            'signature': signature
        }
        response = requests.post(f"http://{server_address}/data/delete", json=json)
        return response

    def read_data(self, server_address, data_url, address_index=0):
        """

        :param server_address:
        :param data_url:
        :param address_index:
        :return:
        """
        signature = self._account.sign_message(str(data_url), address_index)
        json = {
            'data_url': data_url,
            'signature': signature
        }
        requests.post(f"http://{server_address}/data/read", json=json)
        return


if __name__ == '__main__':
    client = Client()
    #print(1)
    client.create_address()
    #print(2)
    #print(client.to_json())
    #print(3)
    client.store_account()
    #print(4)
    client.load_account()
    #print(5)
    #print(client.to_json())
