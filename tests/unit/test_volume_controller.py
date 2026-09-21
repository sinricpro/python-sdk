"""Volume request dispatch and the absolute volume reported back to SinricPro."""

import pytest

from sinricpro.core.types import SinricProRequest
from sinricpro.devices.sinric_pro_speaker import SinricProSpeaker
from sinricpro.devices.sinric_pro_tv import SinricProTV

DEVICES = [SinricProTV, SinricProSpeaker]


def volume_request(action: str, volume: int, volume_default: bool | None = None) -> SinricProRequest:
    value: dict[str, object] = {"volume": volume}
    if volume_default is not None:
        value["volumeDefault"] = volume_default
    return SinricProRequest(action=action, request_value=value)


@pytest.mark.parametrize("create_device", DEVICES)
@pytest.mark.parametrize("volume", [0, 50, 100])
async def test_set_volume_dispatches_to_on_volume(create_device, volume):
    device = create_device("test-device")
    seen = []
    adjusted = []
    device.on_volume(lambda v: _record(seen, v))
    device.on_adjust_volume(lambda v: _record(adjusted, v))
    request = volume_request("setVolume", volume)

    assert await device.handle_request(request) is True
    assert seen == [volume]
    assert adjusted == []
    assert request.response_value == {"volume": volume}


@pytest.mark.parametrize("create_device", DEVICES)
@pytest.mark.parametrize("delta", [-5, 0, 5])
async def test_adjust_volume_reports_absolute_volume(create_device, delta):
    device = create_device("test-device")
    current = {"volume": 50}
    seen = []

    async def on_adjust(volume_delta: int) -> dict:
        seen.append(volume_delta)
        current["volume"] += volume_delta
        return {"success": True, "volume": current["volume"]}

    device.on_adjust_volume(on_adjust)
    request = volume_request("adjustVolume", delta, volume_default=False)

    assert await device.handle_request(request) is True
    # The delta arrives from the request's "volume" field, not "volumeDelta".
    assert seen == [delta]
    # SinricPro stores this as the device's absolute level, not the delta.
    assert request.response_value == {"volume": 50 + delta}


@pytest.mark.parametrize("create_device", DEVICES)
@pytest.mark.parametrize("delta", [-5, 0, 5])
async def test_adjust_volume_echoes_delta_without_reported_volume(create_device, delta):
    device = create_device("test-device")
    device.on_adjust_volume(lambda _volume_delta: _true())
    request = volume_request("adjustVolume", delta, volume_default=False)

    assert await device.handle_request(request) is True
    assert request.response_value == {"volume": delta}


@pytest.mark.parametrize("create_device", DEVICES)
async def test_adjust_volume_reports_zero(create_device):
    device = create_device("test-device")
    device.on_adjust_volume(lambda _volume_delta: _result({"success": True, "volume": 0}))
    request = volume_request("adjustVolume", -50, volume_default=False)

    assert await device.handle_request(request) is True
    assert request.response_value == {"volume": 0}


@pytest.mark.parametrize("create_device", DEVICES)
async def test_adjust_volume_ignores_volume_on_failure(create_device):
    device = create_device("test-device")
    device.on_adjust_volume(lambda _volume_delta: _result({"success": False, "volume": 55}))
    request = volume_request("adjustVolume", 5, volume_default=False)

    assert await device.handle_request(request) is False
    assert request.response_value == {}


@pytest.mark.parametrize("create_device", DEVICES)
@pytest.mark.parametrize("action", ["setVolume", "adjustVolume"])
async def test_returns_false_without_callback(create_device, action):
    device = create_device("test-device")
    assert await device.handle_request(volume_request(action, 5)) is False


async def _record(sink: list, value: int) -> bool:
    sink.append(value)
    return True


async def _true() -> bool:
    return True


async def _result(value: dict) -> dict:
    return value
