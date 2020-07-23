from multiprocessing import Process

class Program:

    def __init__(self, args):
        super().__init__()
        self.args = args
        self.process = Process(target=self.run)

    def run(self):
        print("Using the default run method. Please override this method to make this subclass functional.")

    def start(self):
        self.process.start()