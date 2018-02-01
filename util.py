from ecdsa import VerifyingKey
from binascii import unhexlify

import time
def is_valid_ip(ip):
    q = ip.split('.')
    return len(q) == 4 and len(list(filter(lambda x: 0 <= x <= 255, map(int, filter(lambda x: x.isdigit(), q))))) == 4


def verify_signature(pubkey, message, signature):
        public_key = VerifyingKey.from_string(unhexlify(pubkey))
        return public_key.verify(signature, message.encode("utf-8"))
