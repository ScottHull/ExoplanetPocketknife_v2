import os
from subprocess import Popen, PIPE, TimeoutExpired
import timeit


class AlphaMELTS:
    """
    Controller class for AlphaMELTS subprocessing
    """

    def __init__(self, alphamelts_path: str):
        self.alphamelts_path = alphamelts_path
        if not self.alphamelts_path.endswith('/'):
            self.alphamelts_path += '/'
        self.alphamelts_package_path = self.alphamelts_path + 'package/'
        self.alphamelts_command_path = self.alphamelts_package_path + 'run-alphamelts.command'
        self.alphamelts = None

    def __open_alphamelts(self, env_file: str):
        """
        Open AlphaMELTS in a subprocess.
        """
        if self.alphamelts is not None:
            raise Exception("AlphaMELTS is already running.")
        self.alphamelts = Popen([self.alphamelts_command_path, "-f", env_file], stdin=PIPE, stdout=PIPE, stderr=PIPE,
                                universal_newlines=True)
        return self.alphamelts

    def send_commands(self, commands: list):
        """
        Send command line arguments to AlphaMELTS.
        """
        if self.alphamelts is None:
            raise Exception("AlphaMELTS is not running.")
        self.alphamelts.communicate(input='\n'.join([b"{c}" for c in commands]))

    def run_alphamelts(self, commands: list):
        """
        Main function for running AlphaMELTS.
        Timeout: https://stackoverflow.com/questions/62379807/how-to-kill-a-subprocess-after-50-seconds
        """

    def write_environment_file(self, settings: dict, fname: str = 'environment.txt'):
        """
        Write an AlphaMELTS environment file as a .txt file.
        Each line should be key: value.
        """
        if not fname.endswith('.txt'):
            fname += '.txt'
        if os.path.exists(self.alphamelts_package_path + fname):
            os.remove(self.alphamelts_package_path + fname)
        with open(self.alphamelts_package_path + fname, 'w') as f:
            f.write(f"!{fname.split('.')[0]}\n")
            for key, value in settings.items():
                f.write(f'{key}\t{value}\n')
        f.close()
