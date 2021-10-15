from util.program import Program

from multiprocessing import Process

class Pipeline(Program):

    def __init__(self, args, programs_classes=[]):
        super().__init__(args)
        self.programs = [p(args) for p in programs_classes]

    def run(self):
        super().run()
        for program in self.programs:
            program.run()
