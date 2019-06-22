import queue


class SinricProCommand:
    def __int__(self):
        self.cmdQueue = queue.Queue()

    def getCommand(self):
        return self.cmdQueue.get()

    def pushCommand(self, cmd):
        self.cmdQueue.put(cmd)

    def getQueueLength(self):
        return self.cmdQueue.qsize()
