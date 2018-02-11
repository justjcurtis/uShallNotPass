import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):


    _pad = lambda self, s: s + (self.bs - len(s) % self.bs) * \
	                   chr(self.bs - len(s) % self.bs).encode()
    _unpad = lambda self, s: s[:-ord(s[len(s) - 1:])]

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raww = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raww))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
