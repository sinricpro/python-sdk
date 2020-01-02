from json import dumps
from base64 import b64encode
import hmac as sinricHmac
from hashlib import sha256


class Signature:
    def __init__(self, secretKey):
        self.secretKey = secretKey

    def verifySignature(self, payload, signature) -> bool:
        self.myHmac = sinricHmac.new(self.secretKey.encode('utf-8'),
                                     dumps(payload, separators=(',', ':')).encode('utf-8'), sha256)
        return b64encode(self.myHmac.digest()).decode('utf-8') == signature

    def getSignature(self, payload) -> dict:
        replyHmac = sinricHmac.new(self.secretKey.encode('utf-8'),
                                   dumps(payload, separators=(',', ':')).encode('utf-8'), sha256)

        encodedHmac = b64encode(replyHmac.digest())

        return {
            "HMAC": encodedHmac.decode('utf-8')
        }
