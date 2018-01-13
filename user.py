from keylib.private_key import ECPrivateKey
from keylib.public_key_encoding import public_key_to_address


class User:

    def __init__(self, private_key=None, public_key=None, address=None):
        if private_key == None:
            self.private_key = ECPrivateKey()
            self.public_key = self.private_key.public_key()
            self.address = self.public_key.address()
        else:
            self.private_key = private_key
            self.public_key = self.private_key.public_key()
            self.address = self.public_key.address()




if __name__ == '__main__':
    p = User()
    print(p.private_key.to_hex())
    print(p.public_key.to_hex())
