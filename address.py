from ecdsa import SigningKey, VerifyingKey


class Address:
    def __init__(self, private_key=None):
        if private_key is None:
            self._private_key = SigningKey.generate()
            self._public_key = self._private_key.get_verifying_key()
            self.address = self._public_key.to_string()
        else:
            self._private_key = private_key
            self._public_key = self.private_key.get_verifying_key()

    def sign_message(self, message):
        return self._private_key.sign(message.encode("utf-8"))

    def sign_authorization(self, auth):
        m = auth.calchash()
        return self.sign_message(m)

    def get_pubkey(self):
        return self._public_key.to_string().hex()


def verify_signature(pubkey, message, signature):
        public_key = VerifyingKey.from_string(pubkey)
        return public_key.verify(signature,message.encode("utf-8"))


if __name__ == '__main__':
    u = Address()
    print(u.address)
    print(u.signMessage("fa9988j"))
    s = u.signMessage("fa9988j")
    p = u.getPubkey()
    print(verifySignature(p,"fa9988j",s))

