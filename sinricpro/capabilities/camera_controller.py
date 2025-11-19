"""
CameraController Capability

Provides camera control functionality including snapshot capture and motion detection.
"""

from typing import Any, Callable, Awaitable, TYPE_CHECKING, Optional
import aiohttp
import time

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

# Type alias for snapshot callback
SnapshotCallback = Callable[[str], Awaitable[bool]]
GetStreamUrlCallback = Callable[[str, str], Awaitable[tuple[bool, str]]]
GetWebRTCAnswerCallback = Callable[[str, str], Awaitable[tuple[bool, str]]]

class CameraController:
    """
    Mixin providing camera control capability.

    Provides methods to handle snapshot requests and send camera events.

    Example:
        >>> class MyCamera(SinricProDevice, CameraController):
        ...     pass
        >>> camera = MyCamera("device_id", "CAMERA")
        >>> async def on_snapshot(device_id: str) -> bool:
        ...     print(f"Snapshot requested for {device_id}")
        ...     # Capture and upload snapshot
        ...     return True
        >>> camera.on_snapshot(on_snapshot)
    """

    # Camera API endpoints
    CAMERA_API_URL = "https://portal.sinric.pro"
    SNAPSHOT_ENDPOINT = "/api/v1/camera/snapshot"
    MOTION_ENDPOINT = "/api/v1/camera/motion"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize CameraController mixin."""
        super().__init__(*args, **kwargs)
        self._snapshot_callback: SnapshotCallback | None = None
        self._camera_stream_url_callback: GetStreamUrlCallback | None = None
        self._camera_webrtc_answer_callback: GetWebRTCAnswerCallback | None = None
        self._camera_event_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_get_stream_url(self, callback: GetStreamUrlCallback) -> None:
        self._camera_stream_url_callback = callback

    def on_get_webrtc_answer(self, callback: GetWebRTCAnswerCallback) -> None:
        self._camera_webrtc_answer_callback = callback

    def on_snapshot(self, callback: SnapshotCallback) -> None:
        """
        Register callback for snapshot requests.

        Args:
            callback: Async function called when snapshot is requested.
                     Receives device_id (str), returns bool (success).

        Example:
            >>> async def handle_snapshot(device_id: str) -> bool:
            ...     # Capture snapshot and upload it
            ...     image_data = capture_image()
            ...     await camera.send_snapshot(image_data)
            ...     return True
            >>> camera.on_snapshot(handle_snapshot)
        """
        self._snapshot_callback = callback

    async def handle_get_webrtc_answer(
        self, offer: str, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        if not self._camera_webrtc_answer_callback:
            SinricProLogger.error(
                f"No get webrtc answer callback registered for {device.get_device_id()}"
            )
            return False, {}

        try:
            success, answer = await self._camera_webrtc_answer_callback(device.get_device_id(), offer)
            if success:
                return True, { "answer" : answer}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in webrtc callback: {e}")
            return False, {}
        
    async def handle_get_camera_stream_url(
        self, protocol: str, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        if not self._camera_stream_url_callback:
            SinricProLogger.error(
                f"No get camera stream url callback registered for {device.get_device_id()}"
            )
            return False, {}

        try:
            success, stream_url = await self._camera_stream_url_callback(device.get_device_id(), protocol)
            if success:
                return True, { "url" : stream_url}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in get camera stream url callback: {e}")
            return False, {}
                
    async def handle_snapshot_request(
        self, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """
        Handle getSnapshot request.

        Args:
            device: The device instance

        Returns:
            Tuple of (success, response_value)
        """
        if not self._snapshot_callback:
            SinricProLogger.error(
                f"No snapshot callback registered for {device.get_device_id()}"
            )
            return False, {}

        try:
            success = await self._snapshot_callback(device.get_device_id())
            if success:
                return True, {}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in snapshot callback: {e}")
            return False, {}

    async def send_snapshot(
        self,
        image_data: bytes,
        content_type: str = "image/jpeg",
    ) -> bool:
        """
        Send a camera snapshot to SinricPro.

        Args:
            image_data: The image data as bytes
            content_type: MIME type of the image (default: image/jpeg)

        Returns:
            True if snapshot was uploaded successfully, False otherwise

        Example:
            >>> with open("snapshot.jpg", "rb") as f:
            ...     image_data = f.read()
            >>> await camera.send_snapshot(image_data)
            True
        """
        if not image_data:
            SinricProLogger.error("No image data provided for snapshot")
            return False

        # Type check - ensure self is a SinricProDevice
        if not hasattr(self, "get_device_id"):
            SinricProLogger.error("CameraController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore

        try:
            # Prepare headers with authentication
            device_id = device.get_device_id()
            timestamp = str(int(time.time()))

            # Get signature from device
            signature = ""
            if hasattr(device, "_client") and hasattr(device._client, "sign_message"):
                signature = device._client.sign_message(device_id + timestamp)

            headers = {
                "x-sinric-deviceid": device_id,
                "x-sinric-createdAt": timestamp,
                "x-sinric-signature": signature,
                "Content-Type": content_type,
            }

            # Upload snapshot
            url = f"{self.CAMERA_API_URL}{self.SNAPSHOT_ENDPOINT}"

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, data=image_data, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        SinricProLogger.info("Snapshot uploaded successfully")
                        return True
                    else:
                        error_text = await response.text()
                        SinricProLogger.error(
                            f"Failed to upload snapshot: {response.status} - {error_text}"
                        )
                        return False

        except Exception as e:
            SinricProLogger.error(f"Error uploading snapshot: {e}")
            return False

    async def send_motion_event(
        self,
        motion_data: Optional[bytes] = None,
        cause: str = "PHYSICAL_INTERACTION"
    ) -> bool:
        """
        Send a motion detection event to SinricPro.

        Args:
            motion_data: Optional motion video/image data as bytes
            cause: Cause of the event (PHYSICAL_INTERACTION or APP_INTERACTION)

        Returns:
            True if event was sent successfully, False if rate limited or failed

        Example:
            >>> # Simple motion event without data
            >>> await camera.send_motion_event()
            True
            >>> # Motion event with video data
            >>> with open("motion.mp4", "rb") as f:
            ...     video_data = f.read()
            >>> await camera.send_motion_event(motion_data=video_data)
            True
        """
        # Check rate limiting
        if not self._camera_event_limiter.can_send_event():
            SinricProLogger.warn("Motion event rate limited")
            return False

        # Type check - ensure self is a SinricProDevice
        if not hasattr(self, "send_event"):
            SinricProLogger.error("CameraController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore

        # If motion data is provided, upload it first
        if motion_data:
            try:
                device_id = device.get_device_id()
                timestamp = str(int(time.time()))

                # Get signature from device
                signature = ""
                if hasattr(device, "_client") and hasattr(device._client, "sign_message"):
                    signature = device._client.sign_message(device_id + timestamp)

                headers = {
                    "x-sinric-deviceid": device_id,
                    "x-sinric-createdAt": timestamp,
                    "x-sinric-signature": signature,
                    "Content-Type": "video/mp4",
                }

                url = f"{self.CAMERA_API_URL}{self.MOTION_ENDPOINT}"

                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url, data=motion_data, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        if response.status != 200:
                            error_text = await response.text()
                            SinricProLogger.error(
                                f"Failed to upload motion data: {response.status} - {error_text}"
                            )
                            return False

            except Exception as e:
                SinricProLogger.error(f"Error uploading motion data: {e}")
                return False

        # Send motion event
        success = await device.send_event(
            action="motion", value={"state": "detected"}, cause=cause
        )

        if success:
            self._camera_event_limiter.event_sent()

        return success
