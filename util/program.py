from multiprocessing import Process

class Program:

    def __init__(self, args):
        super().__init__()
        self.args = args
        self.process = Process(target=self.run)
        self.ran = False

    def run(self):
        self.ran = True

    def start(self):
        self.process.start()
