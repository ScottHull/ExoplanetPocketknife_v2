import os
import csv
import time
from subprocess import Popen, PIPE, TimeoutExpired


class AlphaMELTS:
    """
    Controller class for AlphaMELTS subprocessing
    """

    def __init__(self, alphamelts_path: str, perl_path=None, verbose=True):
        self.alphamelts_path = alphamelts_path
        if not self.alphamelts_path.endswith('/'):
            self.alphamelts_path += '/'
        self.alphamelts_script = 'run-alphamelts.command'
        self.alphamelts_package_path = self.alphamelts_path + 'package/'
        self.alphamelts_command_path = self.alphamelts_package_path + self.alphamelts_script
        self.perl_path = perl_path
        self.alphamelts = None
        self.verbose = verbose
        self.output = None

    # def install_alphamelts(self):
    #     return Popen([self.perl_path, self.alphamelts_package_path + "install2.command"], stdin=PIPE)

    def read_output(self, output_path: str):
        """
        Read in the
        """
        return csv.reader(open(output_path, 'r'))

    def fprint(self, *args):
        if self.verbose:
            print(*args)

    def __open_alphamelts(self, env_file=""):
        """
        Open AlphaMELTS in a subprocess.
        """
        if self.alphamelts is not None:
            raise Exception("AlphaMELTS is already running.")
        popen = [self.alphamelts_command_path]
        # if a Windows OS, prepend the perl path
        if os.name == 'nt':
            popen = [self.perl_path] + popen
        # if an environment file is specified, add it to the command
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

    def get_phase_mass(self, phase: str, output_path: str, row_header="Phase"):
        """
        Gets the mass of a phase from the AlphaMELTS output.
        """
        reader = self.read_output(output_path=output_path)
        found_row = False
        phase_index = None
        mass = 0
        for row in reader:
            if found_row:
                if len(row) == 0:
                    break
                else:
                    mass += float(row[phase_index])
            else:
                if len(row) > 0:
                    if row[0] == row_header:
                        row = next(reader)
                        # get the row index of the phase
                        phase_index = row.index(phase)
                        found_row = True
        self.fprint(f"Mass of {phase}: {mass}")
        return mass

