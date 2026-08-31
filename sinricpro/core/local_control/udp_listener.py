"""
UDP Listener

Receives signed SinricPro commands over the LAN, so a device keeps answering
the app while the cloud is unreachable.
"""

import asyncio
import socket
from typing import Any

from sinricpro.core.message_queue import MessageQueue
from sinricpro.core.types import (
    UDP_MULTICAST_IP,
    UDP_MULTICAST_PORT,
    MessageOrigin,
    QueuedMessage,
    Transport,
)
from sinricpro.utils.logger import SinricProLogger


class _SinricProDatagramProtocol(asyncio.DatagramProtocol):
    """Hands every datagram, with its peer, to the listener."""

    def __init__(self, listener: "UdpListener") -> None:
        self._listener = listener

    def datagram_received(self, data: bytes, addr: tuple[str | Any, ...]) -> None:
        self._listener._on_datagram(data, (str(addr[0]), int(addr[1])))

    def error_received(self, exc: Exception) -> None:
        SinricProLogger.error(f"UDP error: {exc}")

    def connection_lost(self, exc: Exception | None) -> None:
        if exc:
            SinricProLogger.error(f"UDP socket closed: {exc}")


class UdpListener:
    """
    Listens for local control requests on UDP and answers them.

    Joins the SinricPro multicast group and also accepts unicast to this host on
    the same port. Replies leave on the listening socket - a separate send-only
    socket is a known dead end on lwIP stacks and buys nothing here.
    """

    def __init__(
        self,
        receive_queue: MessageQueue,
        interface_ip: str | None = None,
        multicast_ip: str = UDP_MULTICAST_IP,
        port: int = UDP_MULTICAST_PORT,
    ) -> None:
        """
        Initialize the listener.

        Args:
            receive_queue: Queue that received requests are pushed onto
            interface_ip: IPv4 address of the interface to join the group on.
                None lets the OS pick, which is wrong often enough on
                multi-homed hosts to be worth configuring.
            multicast_ip: Multicast group to join
            port: UDP port to listen on
        """
        self.receive_queue = receive_queue
        self.interface_ip = interface_ip
        self.multicast_ip = multicast_ip
        self.port = port
        self._transport: asyncio.DatagramTransport | None = None

    async def start(self) -> bool:
        """
        Bind the socket and join the multicast group.

        Returns:
            True if the listener is up, False if local control is unavailable

        Example:
            >>> listener = UdpListener(receive_queue)
            >>> await listener.start()
        """
        if self._transport is not None:
            return True

        sock: socket.socket | None = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if hasattr(socket, "SO_REUSEPORT"):
                try:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                except OSError:
                    pass  # not honoured on every platform; SO_REUSEADDR is enough

            # Bind to INADDR_ANY, not the group: unicast to this host on the
            # same port must be received too.
            sock.bind(("", self.port))

            mreq = socket.inet_aton(self.multicast_ip) + socket.inet_aton(
                self.interface_ip or "0.0.0.0"
            )
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            sock.setblocking(False)

            loop = asyncio.get_running_loop()
            transport, _ = await loop.create_datagram_endpoint(
                lambda: _SinricProDatagramProtocol(self), sock=sock
            )
            self._transport = transport
        except OSError as e:
            # A failed group join leaves nothing listening; say so rather than
            # letting local control be silently dead.
            if sock is not None:
                sock.close()
            SinricProLogger.error(
                f"Could not listen on UDP {self.port} ({self.multicast_ip}), "
                f"local control unavailable: {e}"
            )
            return False

        SinricProLogger.info(
            f"Local control listening on UDP {self.port}, joined {self.multicast_ip}"
            + (f" on {self.interface_ip}" if self.interface_ip else "")
        )
        return True

    def is_running(self) -> bool:
        """
        Check whether the listener is bound.

        Returns:
            True if the socket is open
        """
        return self._transport is not None

    def _on_datagram(self, data: bytes, peer: tuple[str, int]) -> None:
        """Queue a received request together with the peer that sent it."""
        try:
            message = data.decode("utf-8")
        except UnicodeDecodeError:
            SinricProLogger.error(f"Discarding non-UTF-8 datagram from {peer[0]}:{peer[1]}")
            return

        SinricProLogger.debug(f"UDP request from {peer[0]}:{peer[1]}: {message}")
        self.receive_queue.push_sync(
            QueuedMessage(message, MessageOrigin(Transport.UDP, peer))
        )

    def send(self, message: str, peer: tuple[str, int] | None) -> None:
        """
        Send a reply back to the peer that made the request.

        Args:
            message: The serialized, signed response
            peer: (host, port) the request came from
        """
        if not peer or not peer[1]:
            SinricProLogger.error("UDP message has no peer to answer, dropping")
            return
        if self._transport is None:
            SinricProLogger.error("UDP listener is not running, dropping reply")
            return

        try:
            self._transport.sendto(message.encode("utf-8"), peer)
            SinricProLogger.debug(f"UDP reply to {peer[0]}:{peer[1]}: {message}")
        except OSError as e:
            SinricProLogger.error(f"UDP reply to {peer[0]}:{peer[1]} failed: {e}")

    async def stop(self) -> None:
        """Close the socket and leave the multicast group."""
        if self._transport is None:
            return
        self._transport.close()
        self._transport = None
        SinricProLogger.info("Local control listener stopped")
