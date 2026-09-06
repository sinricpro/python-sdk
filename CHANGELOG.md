## [6.0.0]
- feat: Local control. Devices answer signed commands over the LAN on UDP 3333 (multicast 224.9.9.9, unicast too), so they keep working with the cloud unreachable. Requests dispatch through the existing capability callbacks.
- feat: mDNS announcement of `_sinricpro._udp.local.` (TXT: `deviceIds`, `sdk`, `udp`) for app discovery. `zeroconf` is a required dependency, so a default install announces without extra steps. Local control is on by default; set `local_control=False` to opt out.
- feat: `SinricProConfig.local_control`, `.mdns` and `.local_control_interface` to configure the feature out or pin it to a LAN interface on multi-homed hosts.
- fix: Signatures are now verified against the bytes received, sliced between `"payload":` and `,"signature"`, instead of re-serializing the parsed message. A sender using different key order or spacing was rejected before.
- fix: Outgoing messages are signed over the exact bytes transmitted - the payload is serialized once and spliced into the envelope.
- fix: The send queue is gated per message rather than as a whole, so a cloud message waiting on the socket no longer blocks a LAN reply queued behind it.
- fix: A request that fails verification is answered with a signed "Signature is invalid" response, letting a client tell a wrong app secret from an unreachable device.
- change: `begin()` no longer raises when the cloud is unreachable. The SDK starts, retries in the background and keeps answering local control; only invalid configuration raises. Call `is_connected()` for cloud state. Callers that relied on `begin()` raising to detect an outage must check it instead.


How Local control works:

- Listens on UDP port `3333`, joined to multicast group `224.9.9.9`, and answers
  unicast to this host on the same port.
- Every request is HMAC-SHA256 verified with your `APP_SECRET`; responses are signed
  the same way and go back only to the peer that asked. LAN responses are never
  echoed to the cloud.
- A request that fails verification is answered with `"Signature is invalid"` rather
  than dropped, so a client can tell a wrong secret from an unreachable device.
- The host announces `_sinricpro._udp.local.` over mDNS with TXT records
  `deviceIds`, `sdk` and `udp=1`, refreshed whenever the device list changes.

Check the announcement from another machine on the same network:

```bash
avahi-browse -r _sinricpro._udp          # Linux
dns-sd -B _sinricpro._udp                # macOS / Windows (Bonjour)
```

### Configuration

```python
config = SinricProConfig(
    app_key="your-app-key",
    app_secret="your-app-secret",
    local_control=True,               # False disables LAN control entirely
    mdns=True,                        # False keeps UDP but skips the announcement
    local_control_interface=None,     # pin to a LAN interface, e.g. "192.168.1.50"
)
```

Set `local_control_interface` on hosts with several interfaces (Docker, VPN, WSL).
Left unset, the SDK joins the group on the interface the OS picks and announces the
address of the default route, which is not always the LAN you want.

Without `zeroconf` installed the SDK logs a warning and skips the announcement only -
UDP control still works for a client that knows the device address.

## [5.3.2]
- feat: version number

## [5.3.1]
- fix: [SinricProBlinds - Alexa: Missing callback function: adjustRangeValue](https://github.com/sinricpro/python-sdk/issues/85)

## [5.2.1]
- fix: [WebSocket pong timeout - connection appears dead - Reconnection loop annoys server](https://github.com/sinricpro/python-sdk/issues/83)
- feat: only after 3 consecutive misses does it close the connection

## [5.2.0]
- feat: Send a device setting event to SinricPro

## [5.1.1]
- feat: Module settings commands.
- fix: Missing scope in response.
- fix: Missing mac in websocket header.

## [5.0.1]
- fix: [Periodic disconnects of WebSocketClient](https://github.com/sinricpro/python-sdk/issues/79)

## [5.0.0]
- feat: Speaker, GarageDoor examples added.
- feat: setMode, setRangeValue - instance id support added.
- fix: Signature mismatch issue fixed.
- fix: setSetting command response format.

## [4.0.0]

- BREAKING CHANGE: Remove `restoreDeviceStates` in order to change this at device level from server side instead of fixed value in client sdk.

## [3.1.1]

- Fix Logging

## [3.1.0]

- Replaced with new SDK
