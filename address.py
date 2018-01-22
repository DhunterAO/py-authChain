from ecdsa import SigningKey
from binascii import unhexlify
from util import verify_signature


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

    def to_json(self):
        # print(self._private_key.to_string())
        json = {
            "private_key": self._private_key.to_string(),
            "public_key": self._public_key.to_string()
        }
        return json

    def __str__(self):
        return self.get_pubkey()


if __name__ == '__main__':
    u = Address("d32f637a66da5829a007df4de5aa0f1b120c0aa440ad6062")
    s = u.sign_message("fa9988j")
    p = u.get_pubkey()
    print(p)
    print(unhexlify(p))
    print(u.get_prikey())
    print(verify_signature(p, "fa9988j", s))

    u2 = Address("d32f637a66da5829a007df4de5aa0f1b120c0aa440ad6062")
    print(u2.get_pubkey())
    print(verify_signature(u2.get_pubkey(), "fa9988j", s))
