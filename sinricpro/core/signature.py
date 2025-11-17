"""
Message Signature

HMAC-SHA256 signature generation and validation for SinricPro messages.
"""

import base64
import hashlib
import hmac
import json
import re
from typing import Any

from sinricpro.utils.logger import SinricProLogger


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

    def sign(self, message: dict[str, Any]) -> str:
        """
        Generate HMAC-SHA256 signature for a message.

        Args:
            message: The message dict to sign (must have 'payload' key)

        Returns:
            Base64-encoded signature string

        Example:
            >>> sig = Signature("my-secret")
            >>> message = {"payload": {"action": "setPowerState"}}
            >>> signature = sig.sign(message)
            >>> message["signature"] = {"HMAC": signature}
        """
        # Convert payload to JSON string without spaces
        payload_str = json.dumps(message["payload"], separators=(",", ":"), sort_keys=False)

        # Compute HMAC-SHA256
        signature = hmac.new(self.app_secret, payload_str.encode("utf-8"), hashlib.sha256)

        # Base64 encode
        signature_b64 = base64.b64encode(signature.digest()).decode("utf-8")

        # Add signature to message
        if "signature" not in message:
            message["signature"] = {}
        message["signature"]["HMAC"] = signature_b64

        return signature_b64

    def validate(self, message: dict[str, Any] | str) -> bool:
        """
        Validate message signature.

        Args:
            message: Message dict or JSON string containing signature

        Returns:
            True if signature is valid, False otherwise

        Example:
            >>> sig = Signature("my-secret")
            >>> is_valid = sig.validate(message_dict)
        """
        try:
            # Convert to dict if string
            if isinstance(message, str):
                message = json.loads(message)

            # Extract signature from message
            if "signature" not in message or "HMAC" not in message["signature"]:
                SinricProLogger.error("Message missing signature")
                return False

            received_signature = message["signature"]["HMAC"]

            # Extract payload string from original message
            payload_str = self._extract_payload(message)

            if not payload_str:
                SinricProLogger.error("Failed to extract payload for signature validation")
                return False

            # Compute expected signature
            expected_signature = hmac.new(
                self.app_secret, payload_str.encode("utf-8"), hashlib.sha256
            )
            expected_signature_b64 = base64.b64encode(expected_signature.digest()).decode("utf-8")

            # Compare signatures
            is_valid = hmac.compare_digest(received_signature, expected_signature_b64)

            if not is_valid:
                SinricProLogger.error("Signature validation failed")

            return is_valid

        except Exception as e:
            SinricProLogger.error(f"Error validating signature: {e}")
            return False

    def _extract_payload(self, message: dict[str, Any]) -> str:
        """
        Extract payload as JSON string for signature validation.

        Args:
            message: The message dictionary

        Returns:
            JSON string of the payload
        """
        try:
            # For validation, we need to reconstruct the payload exactly as it was signed
            # This means using the same JSON serialization
            return json.dumps(message["payload"], separators=(",", ":"), sort_keys=False)
        except Exception as e:
            SinricProLogger.error(f"Error extracting payload: {e}")
            return ""
