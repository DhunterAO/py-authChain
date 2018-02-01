from address import Address
import logging


class Account:
    def __init__(self):
        self._addressList = []

    def add_address(self, address):
        if address not in self._addressList:
            self._addressList.append(address)
        return

    def get_address(self, index=0):
        return self._addressList[index]

    def add_address_from_private_key(self, private_key):
        address = Address(private_key)
        if address not in self._addressList:
            self._addressList.append(address)
        return

    def delete_address(self, pubkey):
        for address in self._addressList:
            if address.get_pubkey() == pubkey:
                self._addressList.remove(address)
                return
        logging.error("this address is not in the account")
        return

    def create_address(self, private_key=None):
        self._addressList.append(Address(private_key))
        return

    def sign_message(self, message, index=0):
        if index > len(self._addressList):
            logging.error('index out of range')
            return None
        return self._addressList[index].sign_message(message)

    def to_json(self):
        address_list = []
        for address in self._addressList:
            address_list.append(address.to_json())
        json = {
            "address_list": address_list
        }
        return json


if __name__ == '__main__':
    a = Account()
    a.create_address()
    print(a.to_json())
