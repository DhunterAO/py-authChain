from node import Node
from account import Account
from dataURL import DataURL


class Client:
    def __init__(self, account=None):
        self._account = account

    def upload_data(self, server_address, data, data_url=None):
        """
        Upload data to server and get back the dataURL

        :param server_address: x.x.x.x:port
        :param data: data you want to upload
        :param data_url: if you know the data_url, then adjust it, or the server will create one and tell you data_url
        :return: dataURL where the data stores
        """
        pass

    def delete_data(self, server_address, dataURL):
        pass

    def read_data(self, server_address, dataURL):
        pass

