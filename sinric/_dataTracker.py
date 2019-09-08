import json
import os


class DataTracker:
    def __init__(self, enable_track):
        self.enable_track = enable_track
        if os.path.exists('localdata.json'):
            f = open('localdata.json', 'r')
            self.data = json.load(f)
            f.close()
        else:
            f = open('localdata.json', 'w')
            data = {'volume': 0, 'powerLevel': 0, 'brightness': 0, 'colorTemperature': 0, 'temperature': 0,
                    'rangeValue': 0, "bands": {"name": "", "level": 0},"lockState": True}
            json.dump(data, f)
            self.data = data
            f.close()

    @staticmethod
    def readData(key):
        f = open('localdata.json', 'r')
        data = json.load(f).get(key, False)
        f.close()
        return data

    def writeData(self, key, value):
        f = open('localdata.json', 'w')
        self.data.update({key: value})
        json.dump(self.data, f)
        f.close()
