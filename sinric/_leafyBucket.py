import time

class LeakyBucket:
    def __init__(self, bucket_size, drop_in_time, drop_out_time):
        self.bucket_size = bucket_size
        self.drop_in_time = drop_in_time
        self.drop_out_time = drop_out_time
        self.drop_in_bucket = 0
        self.last_drop = 0

    def millis(self):
        return int(round(time.time() * 1000))

    def leakDrops(self):
        actual_millis = self.millis()
        drops_to_leak = round((actual_millis - self.last_drop) / self.drop_out_time)
        if drops_to_leak > 0:
            if self.drop_in_bucket <= drops_to_leak:
                self.drop_in_bucket = 0
            else:
                self.drop_in_bucket = self.drop_in_bucket - drops_to_leak

    def addDrop(self):
        self.leakDrops()
        actual_millis = self.millis()
        if (self.drop_in_bucket < self.bucket_size) and (
                (actual_millis - self.last_drop) > (self.drop_in_bucket + self.drop_in_time)):
            self.drop_in_bucket = self.drop_in_bucket + 1
            self.last_drop = actual_millis
            return True
        if self.drop_in_bucket >= self.bucket_size:
            return False
        return False