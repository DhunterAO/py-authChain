import hashlib
import time

class Block:
    def __init__(self, prev_hash=0, authorizations=[], hash_root=None, now_hash=0, nonce=0):
        self._authorizations = authorizations
        self._hashRoot = hash_root
        self._timestamp = time.time()
        self._prevHash = prev_hash
        self._nowHash = now_hash
        self._nonce = nonce

    def valid(self):
        for authorization in self._authorizations:
            if not authorization.valid():
                return False


    def getHash(self):
        return self._hash

    def getPrevHash(self):
        return self._prevHash

    def getAuthorizations(self):
        return self._authorizations

    def getAutherization(self, index):
        return self._authorizations[index]

    def addAutherization(self, authorization):
        self._authorizations.append(authorization)

    def calcHashRoot(self):
        m = ""
        for authorization in self._authorizations:
            m += str(authorization)
        self._hashRoot = hashlib.sha256(str())

    def calcHash(self):
        self._nowHash = hashlib.sha256(str(self).encode("utf-8")).hexdigest()

    def updateTime(self):
        self._timestamp = time.time()

    def __str__(self):
        return str(self._prevHash, self._nowHash, self._hashRoot, self._nonce)

if __name__ == '__main__':
    block = Block()