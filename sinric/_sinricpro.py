import websocket
import json
from queue import Queue
import time
import asyncio


def SinricPro(apiKey, deviceId, my_q):
    def on_message(ws, message):
        # obj = json.loads(message)
        my_q.put(json.loads(message))
        # print(message)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")
        time.sleep(2)
        initiate()

    def on_open(ws):
        print("### Initiating new websocket connection ###")

    def initiate():
        websocket.enableTrace(False)

        ws = websocket.WebSocketApp("ws://23.95.122.232:3001",
                                    header={'Authorization:' + apiKey,
                                            'deviceids:' + deviceId},
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open

        ws.run_forever()

    initiate()


def Consumer(my_q):
        if my_q.qsize() > 0:
            print('My Consume : ', my_q.get())
            my_q.task_done()
        else:
            print('Queue Empty')
            return
