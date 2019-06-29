from sinric.sinricpro import SinricPro

apiKey = ''
deviceId1 = ''
deviceId2 = ''
deviceId = ';'.join([deviceId1, deviceId2])


def powerState():
    return


if __name__ == '__main__':
    client = SinricPro(apiKey, deviceId)
    client.handle()
