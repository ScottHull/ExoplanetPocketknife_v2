import os
import time
from subprocess import Popen, PIPE, TimeoutExpired
from time import sleep
import timeit


class AlphaMELTS:
    """
    Controller class for AlphaMELTS subprocessing
    """

    def __init__(self, alphamelts_path: str, perl_path: str):
        self.alphamelts_path = alphamelts_path
        if not self.alphamelts_path.endswith('/'):
            self.alphamelts_path += '/'
        self.alphamelts_script = 'run-alphamelts.command'
        self.alphamelts_package_path = self.alphamelts_path + 'package/'
        self.alphamelts_command_path = self.alphamelts_package_path + self.alphamelts_script
        self.perl_path = perl_path
        self.alphamelts = None

    # def install_alphamelts(self):
    #     return Popen([self.perl_path, self.alphamelts_package_path + "install2.command"], stdin=PIPE)

    def __open_alphamelts(self, env_file=""):
        """
        Open AlphaMELTS in a subprocess.
        """
        if self.alphamelts is not None:
            raise Exception("AlphaMELTS is already running.")
        popen = [self.perl_path, self.alphamelts_script]
        if env_file != "":
            popen += ["-f", env_file]

        self.alphamelts = Popen(popen, stdin=PIPE)
        return self.alphamelts

    def send_commands(self, commands: list):
        """
        Send command line arguments to AlphaMELTS.
        """
        if self.alphamelts is None:
            raise Exception("AlphaMELTS is not running.")
        # convert all commands into bytes
        commands = [bytes(str(c), 'utf-8') for c in commands]
        self.alphamelts.communicate(input=b'\n'.join(commands))

    def run_alphamelts(self, commands: list, env_file_path: str):
        """
        Main function for running AlphaMELTS.
        Timeout: https://stackoverflow.com/questions/62379807/how-to-kill-a-subprocess-after-50-seconds
        """
        self.__open_alphamelts(env_file_path)
        self.send_commands(commands)


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
        return self.alphamelts_package_path + fname
