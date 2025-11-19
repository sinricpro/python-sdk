"""SinricProCamera Device"""
from sinricpro.capabilities.camera_controller import CameraController
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotification
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.core.types import SinricProRequest
from sinricpro.core.actions import ACTION_SET_POWER_STATE, ACTION_SET_SETTING, ACTION_GET_SNAPSHOT, ACTION_GET_WEBRTC_ANSWER, ACTION_GET_CAMERA_STREAM_URL


class SinricProCamera(
    SinricProDevice, PowerStateController, SettingController, PushNotification, CameraController
):
    """
    Camera device supporting snapshots, motion detection, and power control.

    Capabilities:
        - Power state control (on/off)
        - Camera control (snapshots)
        - Motion detection events
        - Settings control
        - Push notifications

    Example:
        >>> from sinricpro import SinricPro
        >>> from sinricpro.devices import SinricProCamera
        >>>
        >>> client = SinricPro(app_key="your-app-key", app_secret="your-app-secret")
        >>> camera = client.add_device(SinricProCamera, "device-id")
        >>>
        >>> async def on_power_state(state: bool) -> bool:
        ...     print(f"Camera power: {'On' if state else 'Off'}")
        ...     return True
        >>>
        >>> async def on_snapshot(device_id: str) -> bool:
        ...     print(f"Snapshot requested for {device_id}")
        ...     # Capture image and upload
        ...     image_data = capture_image()
        ...     await camera.send_snapshot(image_data)
        ...     return True
        >>>
        >>> camera.on_power_state(on_power_state)
        >>> camera.on_snapshot(on_snapshot)
        >>>
        >>> await client.connect()
    """

    def __init__(self, device_id: str) -> None:
        """
        Initialize SinricProCamera device.

        Args:
            device_id: The unique device identifier from SinricPro portal
        """
        super().__init__(device_id=device_id, product_type="CAMERA")

    async def handle_request(self, request: SinricProRequest) -> bool:
        """
        Handle incoming requests for the camera device.

        Args:
            request: The incoming request object

        Returns:
            True if request was handled successfully, False otherwise
        """
        if request.action == ACTION_SET_POWER_STATE:
            state = request.request_value.get("state") == "On"
            success, response_value = await self.handle_power_state_request(state, self)
            request.response_value = response_value
            return success

        elif request.action == ACTION_GET_SNAPSHOT:
            success, response_value = await self.handle_snapshot_request(self)
            request.response_value = response_value
            return success

        elif request.action == ACTION_SET_SETTING:
            setting = request.request_value.get("setting", "")
            value = request.request_value.get("value")
            success, response_value = await self.handle_setting_request(setting, value, self)
            request.response_value = response_value
            return success

        elif request.action == ACTION_GET_WEBRTC_ANSWER:
            offer = request.request_value.get("offer", "")
            success, response_value = await self.handle_get_webrtc_answer(offer, self)
            request.response_value = response_value
            return success
        
        elif request.action == ACTION_GET_CAMERA_STREAM_URL:
            protocol = request.request_value.get("protocol", "")
            success, response_value = await self.handle_get_camera_stream_url(protocol, self)
            request.response_value = response_value
            return success
        request.error_message = f"Missing callback function: {request.action}"
        return False
