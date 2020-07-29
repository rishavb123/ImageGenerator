from multiprocessing import Process

class Program:

    def __init__(self, args):
        super().__init__()
        self.args = args
        self.process = Process(target=self.run)
        self.ran = False
        self.should_log = 'log' not in args or args['log']

    def log(self, *args, **kwargs):
        if self.should_log:
            print(*args, **kwargs)

    def run(self):
        self.ran = True

    def start(self):
        self.process.start()
