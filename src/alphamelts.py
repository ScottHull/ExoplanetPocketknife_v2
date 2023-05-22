from subprocess import Popen, PIPE, TimeoutExpired
import timeit


class AlphaMELTS:
    """
    Controller class for AlphaMELTS subprocessing
    """

    def __init__(self, alphamelts_path: str):
        self.alphamelts_path = alphamelts_path
        self.alphamelts = None

    def __open_alphamelts(self):
        """
        Open AlphaMELTS in a subprocess.
        """
        self.alphamelts = Popen(self.alphamelts_path, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        return self.alphamelts

    def __send_commands(self, commands: list):
        """
        Send command line arguments to AlphaMELTS.
        """
        for command in commands:
            self.alphamelts.stdin.write(command + '\n')
        self.alphamelts.stdin.close()
        return self.alphamelts

    def run_alphamelts(self, commands: list):
        """
        Main function for running AlphaMELTS.
        Timeout: https://stackoverflow.com/questions/62379807/how-to-kill-a-subprocess-after-50-seconds
        """
