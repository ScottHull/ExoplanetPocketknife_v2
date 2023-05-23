import os

from src.alphamelts import AlphaMELTS
from src.composition import Composition

BULK_EARTH = Composition({
    'Si': 16.1,
    'Mg': 15.4,
    'Fe': 32.0,
    'Ca': 1.71,
    'Al': 1.59,
    'Ti': 810 / 10000,
    'Na': 0.18,
})  # McDonough 2003 Table 3

title = "earth"
fO2_buffer = "5"
fO2_offset = "-1.4"
max_temperature = 1400
min_temperature = 1000


bsp_settings = {
    'Increment Temperature': -5,
    'Initial Pressure': 500,
    'Final Pressure': 500,
    'dp/dt': 0,
    'Mode': "Fractionate Solids",
}

alphaMELTS = AlphaMELTS(
    alphamelts_path=r"C:\Users\Scott\OneDrive\Desktop\alphaMELTS2-master\alphaMELTS2-master",
    perl_path=r"C:\Users\Scott\OneDrive\Desktop\alphaMELTS2-master\alphaMELTS2-master\strawberry-perl-5.32.1.1-64bit-portable\perl\bin\perl.exe"
)

# change working directory to alphamelts package
os.chdir(alphaMELTS.alphamelts_package_path)

bsp_file = alphaMELTS.write_environment_file(
    settings={
        "ALPHAMELTS_CALC_MODE": "MELTS",
        # "ALPHAMELTS_VERSION": "pMELTS",
        "ALPHAMELTS_MODE": "isobaric",
        "ALPHAMELTS_MAXT": 3000,
        "ALPHAMELTS_DELTAT": -2,
        "ALPHAMELTS_MINT": 1020,
        "ALPHAMELTS_FRACTIONATE_SOLIDS": "true",
        "ALPHAMELTS_SAVE_ALL": "true",
        "ALPHAMELTS_SKIP_FAILURE": "true",
        "Suppress": "alloy-liquid"
    },
    fname="bsp_env_file.txt"
)

BULK_EARTH.write_melts_file(title=title, settings=bsp_settings, path=alphaMELTS.alphamelts_package_path)

# format alphaMELTS commands
commands = []
# read in the melts file
commands += [1, title + ".melts"]
# set fO2
commands += [5, fO2_buffer, 7, fO2_offset, 'x']
# adjust min and max temperature
commands += [2, 1, max_temperature, 2, min_temperature, 'x']
# execute

alphaMELTS.run_alphamelts(
    commands=commands,
    env_file_path=bsp_file
)
