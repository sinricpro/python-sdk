"""Local control: message origin, LAN dispatch and the invalid-signature reply."""

import asyncio
import json
import socket
from typing import Any, Iterator

import pytest

from sinricpro.core.local_control.udp_listener import UdpListener
from sinricpro.core.message_queue import MessageQueue
from sinricpro.core.signature import Signature
from sinricpro.core.sinric_pro import SinricPro
from sinricpro.core.types import (
    UDP_MULTICAST_PORT,
    WEBSOCKET_ORIGIN,
    MessageOrigin,
    QueuedMessage,
    SinricProConfig,
    Transport,
)
from sinricpro.devices.sinric_pro_switch import SinricProSwitch

APP_KEY = "8bc4a3fa-1b46-4ff1-9d1a-5ba6bd0a1234"
APP_SECRET = "8bc4a3fa-1b46-4ff1-9d1a-5ba6bd0a1234-1c7fd1c4-2b0e-4a5c-9d9e-9f7c0f9a4321"
DEVICE_ID = "5dc1564130a1b2c3d4e5f607"
PEER = ("192.168.1.42", 51234)


@pytest.fixture
def sinric_pro() -> Iterator[SinricPro]:
    """A SinricPro instance wired up without touching the network."""
    SinricPro._instance = None
    sp = SinricPro.get_instance()
    sp.config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)
    sp.signature = Signature(APP_SECRET)
    yield sp
    SinricPro._instance = None


def build_request(action: str = "setPowerState", value: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "header": {"payloadVersion": 2, "signatureVersion": 1},
        "payload": {
            "action": action,
            "clientId": "alexa-skill",
            "createdAt": 1700000000,
            "deviceId": DEVICE_ID,
            "replyToken": "6f1c0d5e-1a2b",
            "type": "request",
            "value": value if value is not None else {"state": "On"},
        },
    }


def udp_entry(raw: str) -> QueuedMessage:
    return QueuedMessage(raw, MessageOrigin(Transport.UDP, PEER))


class TestQueueOrigin:
    def test_plain_strings_default_to_the_websocket_origin(self) -> None:
        queue = MessageQueue()
        queue.push_sync("hello")

        entry = queue.pop_sync()
        assert entry is not None
        assert entry.message == "hello"
        assert entry.origin == WEBSOCKET_ORIGIN

    def test_peer_is_carried_per_message(self) -> None:
        """Two peers in flight at once must not share one slot on the listener."""
        queue = MessageQueue()
        queue.push_sync(QueuedMessage("a", MessageOrigin(Transport.UDP, ("10.0.0.1", 1111))))
        queue.push_sync(QueuedMessage("b", MessageOrigin(Transport.UDP, ("10.0.0.2", 2222))))

        first = queue.pop_sync()
        second = queue.pop_sync()
        assert first is not None and second is not None
        assert first.origin.peer == ("10.0.0.1", 1111)
        assert second.origin.peer == ("10.0.0.2", 2222)

    def test_pop_skips_entries_the_predicate_rejects(self) -> None:
        queue = MessageQueue()
        queue.push_sync("cloud")
        queue.push_sync(QueuedMessage("lan", MessageOrigin(Transport.UDP, PEER)))

        entry = queue.pop_sync(lambda m: m.origin.transport is Transport.UDP)
        assert entry is not None
        assert entry.message == "lan"
        assert len(queue) == 1

    def test_oldest_entries_are_dropped_past_max_size(self) -> None:
        queue = MessageQueue(max_size=2)
        for i in range(4):
            queue.push_sync(str(i))

        assert [queue.pop_sync().message for _ in range(2)] == ["2", "3"]  # type: ignore[union-attr]


class TestInvalidSignatureReply:
    async def test_udp_request_with_a_bad_signature_gets_a_signed_reply(
        self, sinric_pro: SinricPro
    ) -> None:
        raw = Signature("the-wrong-secret").sign_message(build_request())

        await sinric_pro._handle_message(udp_entry(raw))

        entry = sinric_pro.send_queue.pop_sync()
        assert entry is not None
        assert entry.origin.transport is Transport.UDP
        assert entry.origin.peer == PEER

        response = json.loads(entry.message)
        assert response["payload"]["success"] is False
        assert response["payload"]["message"] == "Signature is invalid"
        assert response["payload"]["replyToken"] == "6f1c0d5e-1a2b"
        # Signed with our secret so the client can tell a wrong secret from silence.
        assert sinric_pro.signature is not None
        assert sinric_pro.signature.validate(entry.message) is True

    async def test_reply_survives_a_request_missing_every_echoed_field(
        self, sinric_pro: SinricPro
    ) -> None:
        raw = '{"header":{},"payload":{"type":"request"},"signature":{"HMAC":"bogus"}}'

        await sinric_pro._handle_message(udp_entry(raw))

        entry = sinric_pro.send_queue.pop_sync()
        assert entry is not None
        assert json.loads(entry.message)["payload"]["message"] == "Signature is invalid"


class TestLanDispatch:
    async def test_udp_request_reaches_the_device_callback(self, sinric_pro: SinricPro) -> None:
        seen: list[bool] = []

        async def on_power_state(state: bool) -> bool:
            seen.append(state)
            return True

        switch = SinricProSwitch(DEVICE_ID)
        switch.on_power_state(on_power_state)
        sinric_pro.add(switch)

        assert sinric_pro.signature is not None
        raw = sinric_pro.signature.sign_message(build_request())
        await sinric_pro._handle_message(udp_entry(raw))

        assert seen == [True]

        entry = sinric_pro.send_queue.pop_sync()
        assert entry is not None
        assert entry.origin == MessageOrigin(Transport.UDP, PEER)
        assert json.loads(entry.message)["payload"]["success"] is True

    async def test_cloud_request_still_answers_over_the_websocket(
        self, sinric_pro: SinricPro
    ) -> None:
        async def on_power_state(state: bool) -> bool:
            return True

        switch = SinricProSwitch(DEVICE_ID)
        switch.on_power_state(on_power_state)
        sinric_pro.add(switch)

        assert sinric_pro.signature is not None
        raw = sinric_pro.signature.sign_message(build_request())
        await sinric_pro._handle_message(QueuedMessage(raw))

        entry = sinric_pro.send_queue.pop_sync()
        assert entry is not None
        assert entry.origin.transport is Transport.WEBSOCKET


class TestSendQueueGating:
    async def test_lan_reply_is_sent_while_the_cloud_is_unreachable(
        self, sinric_pro: SinricPro
    ) -> None:
        """A held cloud message must not block a LAN reply queued behind it."""
        sent: list[tuple[str, tuple[str, int] | None]] = []

        class FakeListener:
            def send(self, message: str, peer: tuple[str, int] | None) -> None:
                sent.append((message, peer))

        sinric_pro.udp_listener = FakeListener()  # type: ignore[assignment]
        sinric_pro.send_queue.push_sync("cloud-event")
        sinric_pro.send_queue.push_sync(QueuedMessage("lan-reply", MessageOrigin(Transport.UDP, PEER)))
        sinric_pro.is_initialized = True

        task = asyncio.create_task(sinric_pro._process_send_queue())
        await asyncio.sleep(0.05)
        sinric_pro.is_initialized = False
        task.cancel()

        assert sent == [("lan-reply", PEER)]
        # The cloud message is held, not dropped.
        assert len(sinric_pro.send_queue) == 1


class TestUdpListener:
    async def test_datagram_is_queued_with_its_peer(self) -> None:
        queue = MessageQueue()
        listener = UdpListener(queue)

        listener._on_datagram(b'{"payload":{}}', PEER)

        entry = queue.pop_sync()
        assert entry is not None
        assert entry.message == '{"payload":{}}'
        assert entry.origin == MessageOrigin(Transport.UDP, PEER)

    async def test_non_utf8_datagram_is_discarded(self) -> None:
        queue = MessageQueue()
        listener = UdpListener(queue)

        listener._on_datagram(b"\xff\xfe\x00", PEER)

        assert queue.is_empty()

    async def test_reply_goes_out_on_the_listening_socket(self) -> None:
        sent: list[tuple[bytes, tuple[str, int]]] = []

        class FakeTransport:
            def sendto(self, data: bytes, addr: tuple[str, int]) -> None:
                sent.append((data, addr))

        listener = UdpListener(MessageQueue())
        listener._transport = FakeTransport()  # type: ignore[assignment]

        listener.send("pong", PEER)
        listener.send("dropped", None)

        assert sent == [(b"pong", PEER)]

    async def test_binds_and_receives_over_the_loopback(self) -> None:
        queue = MessageQueue()
        listener = UdpListener(queue, port=UDP_MULTICAST_PORT)

        if not await listener.start():
            pytest.skip("cannot bind UDP 3333 / join multicast in this environment")

        try:
            sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sender.sendto(b'{"hello":1}', ("127.0.0.1", UDP_MULTICAST_PORT))
            sender.close()

            for _ in range(50):
                if not queue.is_empty():
                    break
                await asyncio.sleep(0.02)
        finally:
            await listener.stop()

        entry = queue.pop_sync()
        assert entry is not None
        assert entry.message == '{"hello":1}'
        assert entry.origin.transport is Transport.UDP
        assert entry.origin.peer is not None
