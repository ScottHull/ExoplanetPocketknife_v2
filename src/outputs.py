import os
import csv

class AbstractOutput:

    def __init__(self, path: str, title: str):
        self.path = path
        self.file = None
        self.title = title

    def read_output(self):
        """
        Read in the
        """
        with open(self.path, 'r') as f:
            reader = csv.reader(f)
            return reader



class BSPOutput(AbstractOutput):

    def __init__(self, path: str, title: str):
        super().__init__(path, title)
