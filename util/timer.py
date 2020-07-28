import time

class Timer(object):

    def __init__(self):
        self.start_time = time.time()
        self.end_time = self.start_time
        self.elapsed_time = 0

    def start(self):
        self.start_time = time.time()
    
    def stop(self):
        self.end_time = time.time()
        self.elapsed_time += self.end_time - self.start_time

    def live(self):
        return self.elapsed_time + time.time() - self.start_time

    def read(self):
        return self.elapsed_time

    @staticmethod
    def s_to_hms(s):
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return h, m, s