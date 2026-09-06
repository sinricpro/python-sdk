"""Signing and verification of the SinricPro message envelope."""

import base64
import hashlib
import hmac
import json

from sinricpro.core.signature import Signature

APP_SECRET = "8bc4a3fa-1b46-4ff1-9d1a-5ba6bd0a1234-1c7fd1c4-2b0e-4a5c-9d9e-9f7c0f9a4321"


def hmac_b64(payload_str: str, secret: str = APP_SECRET) -> str:
    digest = hmac.new(secret.encode(), payload_str.encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def make_request() -> dict[str, object]:
    return {
        "header": {"payloadVersion": 2, "signatureVersion": 1},
        "payload": {
            "action": "setPowerState",
            "clientId": "alexa-skill",
            "createdAt": 1700000000,
            "deviceId": "5dc1564130xxxxxxxxxxxxxx",
            "replyToken": "6f1c0d5e-1a2b",
            "type": "request",
            "value": {"state": "On"},
        },
    }


class TestSigning:
    def test_sign_message_round_trips(self) -> None:
        sig = Signature(APP_SECRET)
        raw = sig.sign_message(make_request())

        assert sig.validate(raw) is True

    def test_signed_bytes_are_the_transmitted_bytes(self) -> None:
        """The HMAC must cover the payload substring that actually goes out."""
        sig = Signature(APP_SECRET)
        message = make_request()
        raw = sig.sign_message(message)

        payload_slice = Signature.extract_payload(raw)
        assert payload_slice in raw
        assert json.loads(raw)["signature"]["HMAC"] == hmac_b64(payload_slice)

    def test_signature_is_last_key(self) -> None:
        """extract_payload() relies on ,"signature" following the payload."""
        raw = Signature(APP_SECRET).sign_message(make_request())

        assert raw.index('"payload":') < raw.index(',"signature"')
        assert raw.endswith("}}")

    def test_envelope_key_order_matches_the_wire_contract(self) -> None:
        raw = Signature(APP_SECRET).sign_message(make_request())

        assert raw.startswith('{"header":{"payloadVersion":2,"signatureVersion":1},"payload":')

    def test_sign_populates_signature_in_place(self) -> None:
        sig = Signature(APP_SECRET)
        message = make_request()
        returned = sig.sign(message)

        assert message["signature"]["HMAC"] == returned  # type: ignore[index]


class TestVerification:
    def test_verifies_by_slicing_received_bytes(self) -> None:
        """A foreign sender's key order and spacing are its own."""
        payload_str = '{"value":{"state":"On"},"action":"setPowerState","deviceId":"abc"}'
        raw = (
            '{"header": {"payloadVersion": 2, "signatureVersion": 1},'
            '"payload":' + payload_str + ','
            '"signature":{"HMAC":"' + hmac_b64(payload_str) + '"}}'
        )

        assert Signature(APP_SECRET).validate(raw) is True

    def test_key_order_independence(self) -> None:
        """Two orderings of the same payload each verify against their own bytes."""
        sig = Signature(APP_SECRET)
        a = '{"action":"setPowerState","deviceId":"abc"}'
        b = '{"deviceId":"abc","action":"setPowerState"}'

        for payload_str in (a, b):
            raw = (
                '{"header":{"payloadVersion":2,"signatureVersion":1},'
                '"payload":' + payload_str + ','
                '"signature":{"HMAC":"' + hmac_b64(payload_str) + '"}}'
            )
            assert sig.validate(raw) is True

    def test_reserializing_a_parsed_dict_would_reject_a_valid_message(self) -> None:
        """Why validation slices: re-encoding imposes our own conventions."""
        payload_str = '{"action": "setPowerState", "deviceId": "abc"}'  # sender used spaces
        raw = (
            '{"header":{"payloadVersion":2,"signatureVersion":1},'
            '"payload":' + payload_str + ','
            '"signature":{"HMAC":"' + hmac_b64(payload_str) + '"}}'
        )
        sig = Signature(APP_SECRET)

        assert sig.validate(raw) is True
        assert sig.validate(json.loads(raw)) is False

    def test_tampered_payload_is_rejected(self) -> None:
        sig = Signature(APP_SECRET)
        raw = sig.sign_message(make_request())
        tampered = raw.replace('"state":"On"', '"state":"Off"')

        assert tampered != raw
        assert sig.validate(tampered) is False

    def test_wrong_secret_is_rejected(self) -> None:
        raw = Signature(APP_SECRET).sign_message(make_request())

        assert Signature("a-different-secret").validate(raw) is False

    def test_missing_signature_is_rejected(self) -> None:
        raw = '{"header":{},"payload":{"action":"setPowerState"}}'

        assert Signature(APP_SECRET).validate(raw) is False

    def test_garbage_is_rejected(self) -> None:
        assert Signature(APP_SECRET).validate("not json at all") is False


class TestExtractPayload:
    def test_returns_the_exact_substring(self) -> None:
        raw = '{"header":{},"payload":{"a":1},"signature":{"HMAC":"x"}}'

        assert Signature.extract_payload(raw) == '{"a":1}'

    def test_returns_empty_when_markers_are_absent(self) -> None:
        assert Signature.extract_payload('{"payload":{"a":1}}') == ""
        assert Signature.extract_payload('{"signature":{}}') == ""
