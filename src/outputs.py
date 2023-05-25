import os
import csv
from src.composition import Composition


class AbstractOutput:

    def __init__(self, path: str, filename: str):
        self.path = path
        self.filename = filename

    def read_output(self):
        """
        Read in the
        """
        with open(self.path, 'r') as f:
            return csv.reader(f)


class BSPOutput(AbstractOutput):

    def __init__(self, path: str, filename: str):
        super().__init__(path, filename)

    def get_phase_mass(self, phase):
        reader = self.read_output()
        found_row = False
        phase_index = None
        mass = 0
        for row in reader:
            if found_row:
                if len(row) == 0:
                    break
                else:
                    mass += float(row[phase_index])
            elif row[0] == "Phase":
                # get the row index of the phase
                phase_index = row.index(phase)
                found_row = True
        return mass

    def get_bsp_composition(self, bulk_planet_composition: Composition):
        """
        Removes the core-bound Fe alloy from the bulk planet composition to get the BSP composition.
        :param bulk_planet_composition:
        :return:
        """
        fe_alloy = self.get_phase_mass("alloy-solid_0")
        bsp_composition = bulk_planet_composition.elements['Fe'] - fe_alloy
        return Composition(bsp_composition)
