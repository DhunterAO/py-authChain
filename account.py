from address import Address
import logging


class Account:
    def __init__(self):
        self._addressList = set()

    def add_address(self, address):
        self._addressList.add(address)
        return

    def delete_address(self, pubkey):
        for address in self._addressList:
            if address.get_pubkey() == pubkey:
                self._addressList.remove(address)
                return
        logging.error("this address is not in the account")
        return

    def create_address(self):
        self._addressList.add(Address())
        return

    def list_address(self):
        for address in self._addressList:
            print(address.get_pubkey())
        return [address.get_pubkey() for address in self._addressList]

    def sign_message(self, message, index):
        if index > len(self._addressList):
            logging.error('index out of range')
            return None
        return list(self._addressList)[index].sign_message(message)


if __name__ == '__main__':
    a = Account()
    a.list_address()
    a.create_address()
    a.list_address()
    a.create_address()
    b = a.list_address()[1]
    a.delete_address(b)
    a.list_address()
