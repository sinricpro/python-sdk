"""
mDNS Announcer

Publishes ``_sinricpro._udp.local.`` so the app can find this host on the LAN
without asking the cloud for its address.

Requires the optional ``zeroconf`` dependency (``pip install sinricpro[mdns]``).
Without it local control still works - the app falls back to the address the
cloud reported for the device.
"""

import socket
from typing import Any

from sinricpro.core.types import MDNS_SERVICE_TYPE, UDP_MULTICAST_PORT
from sinricpro.utils.logger import SinricProLogger
from sinricpro.utils.network import get_local_ip, get_mdns_host_name

try:
    from zeroconf import IPVersion, ServiceInfo
    from zeroconf.asyncio import AsyncZeroconf

    ZEROCONF_AVAILABLE = True
except ImportError:  # pragma: no cover - depends on the install extras
    ZEROCONF_AVAILABLE = False


class MdnsAnnouncer:
    """
    Announces this host as a SinricPro local control endpoint.

    TXT records:
        deviceIds  comma-separated ids this host answers for
        sdk        SDK version
        udp        always "1"

    The record is refreshed when the device list changes - not on a timer and
    not on every reconnect.
    """

    def __init__(
        self,
        sdk_version: str,
        interface_ip: str | None = None,
        port: int = UDP_MULTICAST_PORT,
        host_name: str | None = None,
    ) -> None:
        """
        Initialize the announcer.

        Args:
            sdk_version: Value of the ``sdk`` TXT record
            interface_ip: IPv4 address to announce. None discovers the interface
                carrying the default route.
            port: UDP port to advertise
            host_name: mDNS host label; defaults to ``sinricpro-<mac>``
        """
        self.sdk_version = sdk_version
        self.interface_ip = interface_ip
        self.port = port
        self.host_name = host_name or get_mdns_host_name()
        self._zeroconf: Any = None
        self._info: Any = None
        self._device_ids: str = ""

    def _build_info(self, device_ids: str) -> Any:
        return ServiceInfo(
            MDNS_SERVICE_TYPE,
            f"{self.host_name}.{MDNS_SERVICE_TYPE}",
            addresses=[socket.inet_aton(self.interface_ip)] if self.interface_ip else [],
            port=self.port,
            properties={
                "deviceIds": device_ids,
                "sdk": self.sdk_version,
                "udp": "1",
            },
            server=f"{self.host_name}.local.",
        )

    async def start(self, device_ids: list[str]) -> bool:
        """
        Register the service.

        Args:
            device_ids: Device ids this host answers for

        Returns:
            True if the service was registered
        """
        if not ZEROCONF_AVAILABLE:
            SinricProLogger.warn(
                "zeroconf is not installed, skipping mDNS announcement "
                "(local control still works via the cloud-reported address). "
                "Install with: pip install sinricpro[mdns]"
            )
            return False

        if self._zeroconf is not None:
            return True

        if not self.interface_ip:
            self.interface_ip = get_local_ip()
        if not self.interface_ip:
            SinricProLogger.warn(
                "Could not determine a LAN address, skipping mDNS announcement"
            )
            return False

        self._device_ids = ",".join(device_ids)

        try:
            self._zeroconf = AsyncZeroconf(
                interfaces=[self.interface_ip], ip_version=IPVersion.V4Only
            )
            self._info = self._build_info(self._device_ids)
            await self._zeroconf.async_register_service(self._info)
        except Exception as e:
            SinricProLogger.error(f"mDNS announcement failed: {e}")
            await self.stop()
            return False

        SinricProLogger.info(
            f"Announced {MDNS_SERVICE_TYPE} as {self.host_name}.local. "
            f"on {self.interface_ip}:{self.port} deviceIds={self._device_ids}"
        )
        return True

    async def update(self, device_ids: list[str]) -> None:
        """
        Re-announce, but only if the device list actually changed.

        Args:
            device_ids: Device ids this host answers for
        """
        joined = ",".join(device_ids)
        if self._zeroconf is None or joined == self._device_ids:
            return

        self._device_ids = joined
        try:
            self._info = self._build_info(joined)
            await self._zeroconf.async_update_service(self._info)
            SinricProLogger.info(f"mDNS deviceIds updated: {joined}")
        except Exception as e:
            SinricProLogger.error(f"mDNS update failed: {e}")

    async def stop(self) -> None:
        """Unregister the service and close the responder."""
        if self._zeroconf is None:
            return
        try:
            if self._info is not None:
                await self._zeroconf.async_unregister_service(self._info)
            await self._zeroconf.async_close()
        except Exception as e:
            SinricProLogger.error(f"mDNS shutdown failed: {e}")
        finally:
            self._zeroconf = None
            self._info = None
