import re
import pandas as pd

def get_molecule_stoichiometry(molecule: str):
    """
    Given a molecule, return the stoichiometry of the molecule.
    return type: dict
    """
    stoich = re.findall(r'([A-Z][a-z]*)(\d*)', molecule)
    d = {}
    for i in stoich:
        d.update({i[0]: i[1]})
        if d[i[0]] == '':
            d[i[0]] = 1
        d[i[0]] = int(d[i[0]])
    return d


class Composition:

    def __init__(self):
        self.periodic_table = pd.read_csv("data/periodic_table.csv", index_col=0)

    def get_molecule_mass(self, molecule: str):
        """
        Given a molecule and a dictionary of element masses, return the mass of the molecule.
        return type: float
        """
        stoich = get_molecule_stoichiometry(molecule)
        mass = 0
        for element in stoich:
            mass += stoich[element] * self.periodic_table.loc[element, 'atomic_mass']
        return mass
