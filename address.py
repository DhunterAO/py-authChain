from ecdsa import SigningKey, VerifyingKey
from binascii import unhexlify
from util import verify_signature

import logging


class Address:
    def __init__(self, private_key=None):
        if private_key is None:
            self._private_key = SigningKey.generate()
            self._public_key = self._private_key.get_verifying_key()
        else:
            self._private_key = SigningKey.from_string(unhexlify(private_key))
            self._public_key = self._private_key.get_verifying_key()

    def sign_message(self, message):
        return self._private_key.sign(message.encode("utf-8"))

    def sign_authorization(self, auth):
        m = auth.calchash()
        return self.sign_message(m)

    def get_pubkey(self):
        return self._public_key.to_string().hex()

    def get_prikey(self):
        return self._private_key.to_string().hex()

    def valid(self):
        return self._public_key.to_string() == self._private_key.get_verifying_key().to_string()

    def to_json(self):
        json = {
            "public_key": self._public_key.to_string().hex(),
            "private_key": self._private_key.to_string().hex()
        }
        return json

    def from_json(self, json):
        required = ['public_key', 'private_key']
        if not all(k in json for k in required):
            logging.warning(f'value missing in {required}')
            return False

        if not isinstance(json["public_key"], str) or not isinstance(json['private_key'], str):
            logging.warning('public_key and private_key should be both type<str>')
            return False

        self._public_key = VerifyingKey.from_string(unhexlify(json["public_key"]))
        self._private_key = SigningKey.from_string(unhexlify(json["private_key"]))
        return self.valid()

    def __str__(self):
        return self.get_pubkey()


if __name__ == '__main__':
    u = Address("d32f637a66da5829a007df4de5aa0f1b120c0aa440ad6062")
    print(u.to_json())
    print(u.valid())

    v = Address()
    print(v.from_json(u.to_json()))
    print(v.to_json())
