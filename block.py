import hashlib
import time
import logging

from authorization import Authorization


class Block:
    def __init__(self, prev_hash="fff", authorizations=None, hash_root="5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9",
                 timestamp=None, now_hash="fff", nonce=0):
        if authorizations is None:
            self._authorizations = []
        else:
            self._authorizations = authorizations
        self._hashRoot = hash_root
        if timestamp is None:
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
                print("1")
                return False
        if self.calc_hash_root() != self._hashRoot:
            print("2")
            return False
        if self.calc_hash() != self._nowHash:
            print("3")
            print(self.calc_hash())
            print(self._nowHash)
            return False
        now = time.time()
        if self._timestamp > now+600:
            print("4")
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
        m = "5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9"
        for authorization in self._authorizations:
            m += str(authorization)
            m = hashlib.sha256(m.encode()).hexdigest()
        return m

    def set_hash_root(self):
        self._hashRoot = self.calc_hash_root()

    def get_timestamp(self):
        return self._timestamp

    def calc_hash(self):
        return hashlib.sha256(str(self).encode()).hexdigest()

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
        self.set_now_hash()
        return

    def to_json(self):
        json = {
            'prev_hash': self._prevHash,
            'now_hash': self._nowHash,
            'timestamp': self._timestamp,
            'hash_root': self._hashRoot,
            'nonce': self._nonce,
            'authorizations': []
        }
        for authorization in self._authorizations:
            json['authorizations'].append(authorization.to_json())
        # print(json['authorizations'])
        return json

    def from_json(self, json):
        required = ['prev_hash', 'now_hash', 'timestamp', 'hash_root', 'nonce', 'authorizations']
        if not all(k in json for k in required):
            logging.warning(f'value missing in {required}')
            return False

        if not isinstance(json['prev_hash'], str) or not isinstance(json['now_hash'], str) \
                or not isinstance(json['timestamp'], float) or not isinstance(json['hash_root'], str) \
                or not isinstance(json['nonce'], int) or not isinstance(json['authorizations'], list):
            logging.warning("prev_hash, now_hash and hash_root should be both type<str>, "
                            "timestamp should be type<float>, nonce should be type<int> "
                            "and authorizations should be type<list>")
            return False

        authorizations = []
        for auth in json['authorizations']:
            a = Authorization()
            if not a.from_json(auth):
                return False
            authorizations.append(a)

        self._prevHash = json['prev_hash']
        self._nowHash = json['now_hash']
        self._timestamp = json['timestamp']
        self._hashRoot = json['hash_root']
        self._nonce = json['nonce']
        self._authorizations = authorizations
        return True

    def __str__(self):
        return str(self._prevHash) + str(self._hashRoot) + str(self._nonce) + str(self._timestamp)


if __name__ == '__main__':
    block = Block()
    print(block.to_json())

    b = Block()
    print(b.to_json())
    print(b.from_json(block.to_json()))
    print(b.to_json())
