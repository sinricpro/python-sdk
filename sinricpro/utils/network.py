"""
Network Helpers

Host identity and interface discovery shared by the websocket client and the
local control listener.
"""

import socket
import uuid


def get_mac_address() -> str:
    """Get the MAC address of this machine.

    Returns:
        MAC address string in format XX:XX:XX:XX:XX:XX
    """
    mac = uuid.getnode()
    return ":".join(f"{(mac >> (8 * i)) & 0xFF:02X}" for i in range(5, -1, -1))


def get_mdns_host_name() -> str:
    """Get the mDNS host label for this machine.

    Returns:
        ``sinricpro-<mac, lowercase, no separators>``
    """
    return "sinricpro-" + get_mac_address().replace(":", "").lower()


def get_local_ip() -> str | None:
    """Get the IPv4 address of the interface that carries the default route.

    A multi-homed host (Docker, VPN, WSL) has several; this picks the one the
    OS would use to reach off-box, which is the LAN interface in the common
    case. No packet is sent - the socket is only connected to pick a route.

    Returns:
        The interface address, or None if it could not be determined
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 53))
        return str(sock.getsockname()[0])
    except OSError:
        return None
    finally:
        sock.close()
