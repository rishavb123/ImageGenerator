"""This file contains the Program class"""
from multiprocessing import Process

class Program:
    """A class that fills contains methods that are useful for programs in this project to have"""

    def __init__(self, args):
        super().__init__()
        self.args = args
        self.process = Process(target=self.run)
        self.ran = False

    def run(self):
        """The main method for this instance of the program class."""
        self.ran = True

    def start(self):
        """Runs the run method in a seperate process (enables multiprocessing)"""
        self.process.start()
