from node import Node
import requests
import logging


class Client:
    def __init__(self, account=None, node=Node()):
        self._account = account
        self._node = node

        @self._node.app("/")
        def hello():
            return

    def upload_data(self, server_address, data, data_url=None, address_index=0):
        """
        Upload data to server and get back the dataURL

        :param server_address: x.x.x.x:port
        :param data: data you want to upload
        :param data_url: if you know the data_url, then adjust it, or the server will create one and tell you data_url
        :param address_index: address index in address_list
        :return: dataURL where the data stores
        """
        signature = self._account.sign_message(str(data)+str(data_url), address_index)
        json = {
            'data': data,
            'data_url': data_url,
            'signature': signature
        }
        response = requests.post(server_address, json=json)
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
        response = requests.post(server_address, json=json)
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
        requests.post(server_address, json=json)
        return

    def start_server(self, port=5000):
        self._node.start(port)
        return


