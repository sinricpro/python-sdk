from json import dumps
from base64 import b64encode
import hmac as sinricHmac
from hashlib import sha256


class Signature:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def verify_signature(self, payload, signature) -> bool:
        self.hmac = sinricHmac.new(self.secret_key.encode('utf-8'),
                                   dumps(payload, separators=(',', ':')).encode('utf-8'), sha256)
        return b64encode(self.hmac.digest()).decode('utf-8') == signature

    def get_signature(self, payload) -> dict:
        reply_hmac = sinricHmac.new(self.secret_key.encode('utf-8'),
                                    dumps(payload, separators=(',', ':')).encode('utf-8'), sha256)

        encoded_hmac = b64encode(reply_hmac.digest())

        return {
            "HMAC": encoded_hmac.decode('utf-8')
        }
