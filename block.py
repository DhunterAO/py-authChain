import hashlib
import time


class Block:
    def __init__(self, prev_hash=0, authorizations=[], hash_root=None, timestamp=0, now_hash=0, nonce=0):
        self._authorizations = authorizations
        self._hashRoot = hash_root
        if timestamp == 0:
            self._timestamp = time.time()
        else:
            self._timestamp = timestamp
        self._prevHash = prev_hash
        self._nowHash = now_hash
        self._nonce = nonce
        return

    def valid(self, blockchain):
        for authorization in self._authorizations:
            if not authorization.valid(blockchain):
                return False
        if self.calc_hash_root() != self._hashRoot:
            return False
        if self.calc_hash() != self._nowHash:
            return False
        now = time.time()
        if self._timestamp > now+600:
            return False
        return True

    def get_now_hash(self):
        return self._nowHash

    def get_prev_hash(self):
        return self._prevHash

    def get_authorizations(self):
        return self._authorizations

    def get_authorization(self, index):
        return self._authorizations[index]

    def add_authorization(self, authorization):
        self._authorizations.append(authorization)
        return

    def calc_hash_root(self):
        m = ""
        for authorization in self._authorizations:
            m += str(authorization)
            m = hashlib.sha256(m.encode("utf-8")).hexdigest()
        return m

    def set_hash_root(self):
        self._hashRoot = self.calc_hash_root()

    def get_timestamp(self):
        return self._timestamp

    def calc_hash(self):
        return hashlib.sha256(str(self).encode("utf-8")).hexdigest()

    def set_now_hash(self):
        self._nowHash = self.calc_hash()
        return

    def update_time(self):
        self._timestamp = time.time()
        return

    def update(self):
        self._nonce += 1
        self._nonce %= 4294967296
        if self._nonce == 0:
            self.update_time()
        return

    def __str__(self):
        return str(self._prevHash) + str(self._nowHash) + str(self._hashRoot) + str(self._nonce)


if __name__ == '__main__':
    block = Block()
