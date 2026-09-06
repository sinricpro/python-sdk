"""
Message Signature

HMAC-SHA256 signature generation and validation for SinricPro messages.
"""

import base64
import hashlib
import hmac
import json
from typing import Any

from sinricpro.utils.logger import SinricProLogger

# The envelope is sliced, never re-parsed, so these markers are part of the wire
# contract: the payload is delimited by them and the signature always follows it.
_PAYLOAD_MARKER = '"payload":'
_SIGNATURE_MARKER = ',"signature"'


class Signature:
    """
    Handles HMAC-SHA256 signature generation and validation.

    Signs outgoing messages and validates incoming messages from SinricPro.
    """

    def __init__(self, app_secret: str) -> None:
        """
        Initialize the Signature handler.

        Args:
            app_secret: The SinricPro app secret key
        """
        self.app_secret = app_secret.encode("utf-8")

    def _hmac_b64(self, payload_str: str) -> str:
        """Compute the base64 HMAC-SHA256 of an already serialized payload."""
        digest = hmac.new(self.app_secret, payload_str.encode("utf-8"), hashlib.sha256)
        return base64.b64encode(digest.digest()).decode("utf-8")

    def sign(self, message: dict[str, Any]) -> str:
        """
        Generate HMAC-SHA256 signature for a message.

        Args:
            message: The message dict to sign (must have 'payload' key)

        Returns:
            Base64-encoded signature string

        Note:
            Prefer :meth:`sign_message`, which returns the exact bytes to
            transmit. Serializing the payload a second time to build the
            envelope is what signature mismatches are made of.

        Example:
            >>> sig = Signature("my-secret")
            >>> message = {"payload": {"action": "setPowerState"}}
            >>> signature = sig.sign(message)
            >>> message["signature"] = {"HMAC": signature}
        """
        payload_str = json.dumps(message["payload"], separators=(",", ":"), sort_keys=False)
        signature_b64 = self._hmac_b64(payload_str)

        if "signature" not in message:
            message["signature"] = {}
        message["signature"]["HMAC"] = signature_b64

        return signature_b64

    def sign_message(self, message: dict[str, Any]) -> str:
        """
        Sign a message and return the exact string to transmit.

        The payload is serialized once and spliced into the envelope, so the
        bytes on the wire are byte-for-byte the bytes that were signed. The
        signature is always emitted last, which is what lets a receiver find the
        payload by slicing between the markers.

        Args:
            message: The message dict to sign (must have 'payload' key)

        Returns:
            The serialized, signed message

        Example:
            >>> sig = Signature("my-secret")
            >>> sig.sign_message({"header": {}, "payload": {"action": "setPowerState"}})
        """
        payload_str = json.dumps(message["payload"], separators=(",", ":"), sort_keys=False)
        signature_b64 = self._hmac_b64(payload_str)

        if "signature" not in message:
            message["signature"] = {}
        message["signature"]["HMAC"] = signature_b64

        parts = [
            json.dumps(key) + ":" + json.dumps(value, separators=(",", ":"), sort_keys=False)
            for key, value in message.items()
            if key not in ("payload", "signature")
        ]
        parts.append(_PAYLOAD_MARKER + payload_str)
        parts.append(
            '"signature":' + json.dumps(message["signature"], separators=(",", ":"))
        )
        return "{" + ",".join(parts) + "}"

    def validate(self, message: dict[str, Any] | str) -> bool:
        """
        Validate message signature.

        Args:
            message: The raw received message, or a parsed message dict

        Returns:
            True if signature is valid, False otherwise

        Note:
            Pass the raw string wherever possible. A parsed dict has already
            lost the sender's key order and spacing, so it can only be validated
            against a re-serialization that assumes our own conventions.

        Example:
            >>> sig = Signature("my-secret")
            >>> is_valid = sig.validate(raw_message_string)
        """
        try:
            if isinstance(message, str):
                raw: str | None = message
                parsed: dict[str, Any] = json.loads(message)
            else:
                raw = None
                parsed = message

            if "signature" not in parsed or "HMAC" not in parsed["signature"]:
                SinricProLogger.error("Message missing signature")
                return False

            received_signature = parsed["signature"]["HMAC"]

            payload_str = (
                self.extract_payload(raw)
                if raw is not None
                else json.dumps(parsed["payload"], separators=(",", ":"), sort_keys=False)
            )

            if not payload_str:
                SinricProLogger.error("Failed to extract payload for signature validation")
                return False

            is_valid = hmac.compare_digest(received_signature, self._hmac_b64(payload_str))

            if not is_valid:
                SinricProLogger.error("Signature validation failed")

            return is_valid

        except Exception as e:
            SinricProLogger.error(f"Error validating signature: {e}")
            return False

    @staticmethod
    def extract_payload(raw: str) -> str:
        """
        Slice the payload out of a received message.

        Args:
            raw: The message exactly as received

        Returns:
            The payload substring, or "" if the markers are not both present
        """
        begin = raw.find(_PAYLOAD_MARKER)
        if begin < 0:
            return ""
        end = raw.find(_SIGNATURE_MARKER, begin)
        if end < 0:
            return ""
        return raw[begin + len(_PAYLOAD_MARKER) : end]
