import os.path
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


def normalize(composition: dict, per_100=True):
    """
    Normalize the composition to 100 wt%.
    """
    total = sum(composition.values())
    for element in composition:
        composition[element] /= total
        if per_100:
            composition[element] *= 100.0
    return composition


class AbstractComposition:

    def __init__(self):
        self.periodic_table = pd.read_csv("data/periodic_table.csv", index_col=0)
        self.oxides = pd.read_csv("data/oxides.csv", index_col=0)

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

    def get_corresponding_oxide(self, element: str):
        """
        Gets the corresponding oxide given an element.
        """
        return self.oxides.loc[element, 'oxide']

    def _write_melts_file(self, composition: dict, title: str, settings: dict, path=""):
        """
        Write the melts file as a .melts file.
        Format is as follows:
        Title: title
        Initial Composition: oxide: value, oxide: value, ...
        setting: value, setting: value, ...
        """
        if not path.endswith("/"):
            path += "/"
        if title.endswith(".melts"):
            title = title.split(".")[0]
        if os.path.exists(path + f"{title}.melts"):
            os.remove(path + f"{title}.melts")
        with open(path + f"{title}.melts", 'w') as f:
            f.write(f"Title: {title}\n")
            for c in composition:
                f.write(f"Initial Composition: {c} {composition[c]}\n")
            for setting in settings:
                f.write(f"{setting}: {settings[setting]}\n")
        f.close()

    def element_wt_to_moles(self, element: str, mass: float):
        """
        Given an element in absolute mass, return the moles of the element.
        """
        return mass / self.periodic_table.loc[element, 'atomic_mass']

    def element_moles_to_oxide_moles(self, element: str, moles: float):
        """
        Given an element in moles, return the moles of the oxide.
        """
        corresponding_oxide = self.get_corresponding_oxide(element)
        oxide_stoich = get_molecule_stoichiometry(corresponding_oxide)
        return moles / oxide_stoich[element]

    def oxide_moles_to_oxide_mass(self, oxide: str, moles: float):
        """
        Given an oxide in moles, return its mass.
        """
        return moles * self.get_molecule_mass(oxide)


class Composition(AbstractComposition):

    def __init__(self, elements: dict):
        super().__init__()
        self.elements = normalize(elements)  # elements given as wt%
        self.file = None

    def elements_wt_pct_to_oxide_wt_pct(self):
        """
        Converts elements wt% to oxide wt%.
        """
        oxide_wt_pct = {self.get_corresponding_oxide(element): None for element in self.elements}
        for element in self.elements:
            element_wt = self.element_wt_to_moles(element, self.elements[element])
            oxide_moles = self.element_moles_to_oxide_moles(element, element_wt)
            oxide_wt = self.oxide_moles_to_oxide_mass(self.oxides.loc[element, 'oxide'], oxide_moles)
            oxide_wt_pct[self.get_corresponding_oxide(element)] = oxide_wt
        return normalize(oxide_wt_pct)

    def write_melts_file(self, title: str, settings: dict, path=""):
        """
        Write the melts file as a .melts file.
        Format is as follows:
        Title: title
        Initial Composition: oxide: value, oxide: value, ...
        setting: value, setting: value, ...
        """
        self._write_melts_file(self.elements_wt_pct_to_oxide_wt_pct(), title, settings, path)

    def adjust_mass(self, element: str, amount: float, method="subtraction"):
        """
        Adjust the mass of an element b
        """
        if method == "subtraction":
            self.elements[element] -= amount
        elif method == "addition":
            self.elements[element] += amount
        elif method == "multiplication":
            self.elements[element] *= amount
        else:
            raise ValueError("Invalid method. Choose between subtraction, addition, and multiplication.")
        self.elements = normalize(self.elements)
        return self.elements
