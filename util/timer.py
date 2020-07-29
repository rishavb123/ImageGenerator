import time

class Timer(object):

    def __init__(self):
        self.start_time = time.time()
        self.end_time = self.start_time
        self.elapsed_time = 0
        self.action = False

    def start(self, action=False):
        self.start_time = time.time()
        if action:
            print('START:', action, '. . .')
            self.action = action
    
    def pause(self):
        self.end_time = time.time()
        self.elapsed_time += self.end_time - self.start_time

    def stop(self):
        self.end_time = time.time()
        self.elapsed_time += self.end_time - self.start_time
        if self.action:
            print('STOP:', self.action)
            self.action = False

    def live(self):
        return self.elapsed_time + time.time() - self.start_time

    def read(self):
        return self.elapsed_time

    def show(self):
        h, m, s = Timer.s_to_hms(self.read())
        print('Finished in {} hours, {} minutes, and {} seconds'.format(h, m, s))

    def reset(self):
        self.elapsed_time = 0

    @staticmethod
    def s_to_hms(s):
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return h, m, s