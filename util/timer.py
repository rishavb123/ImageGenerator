import time

class Timer(object):

    def __init__(self, log=print):
        self.start_time = time.time()
        self.end_time = self.start_time
        self.elapsed_time = 0
        self.action = False
        self.log = log

    def start(self, action=False):
        self.start_time = time.time()
        if action:
            self.log('START:', action, '. . .')
            self.action = action
    
    def pause(self):
        self.end_time = time.time()
        self.elapsed_time += self.end_time - self.start_time

    def stop(self):
        self.end_time = time.time()
        self.elapsed_time += self.end_time - self.start_time
        if self.action:
            self.log('STOP:', self.action)
            self.action = False

    def live(self):
        return self.elapsed_time + time.time() - self.start_time

    def read(self):
        return self.elapsed_time

    def show(self):
        h, m, s = Timer.s_to_hms(self.read())
        self.log('Finished in {} hours, {} minutes, and {} seconds'.format(h, m, s))

    def reset(self):
        self.elapsed_time = 0

    def time(self, f, action=False):
        if action: self.log()
        self.start(action)
        r = f()
        self.stop()
        self.show()
        return r

    @staticmethod
    def s_to_hms(s):
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return h, m, s