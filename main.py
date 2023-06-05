import os

from src.alphamelts import AlphaMELTS
from src.composition import Composition

""""
============================ CURRENT PROBLEMS ============================
    1. alphaMELTS2 may not support bulk planet abundances...perhaps just subtract 33wt% Fe from each composition?
"""

# =================== DEFINE THE COMPOSITIONS ===================
BULK_EARTH = Composition({
    'Si': 16.1,
    'Mg': 15.4,
    'Fe': 32.0,
    'Ca': 1.71,
    'Al': 1.59,
    'Ti': 810 / 10000,
    'Na': 0.18,
})  # McDonough 2003 Table 3

# =================== DEFINE THE SETTINGS ===================

title = "earth"
fO2_buffer = 5
fO2_offset = -1.4
max_temperature = 2500
min_temperature = 1000
delta_T = -10
core_fe_mass = 25.283758

bsp_settings = {
    'Increment Temperature': delta_T,
    'Initial Temperature': max_temperature,
    'Final Temperature': min_temperature,
    'Initial Pressure': 4200,
    'Final Pressure': 4200,
    'dp/dt': 0,
    'Mode': "Fractionate Solids",
}

morb_settings = {
    'Increment Temperature': delta_T,
    'Initial Temperature': max_temperature,
    'Final Temperature': min_temperature,
    'Initial Pressure': 4200,
    'Final Pressure': 4200,
    'dp/dt': 0,
    'Mode': "Fractionate Solids",
}

# =================== INITIATE MELTS ===================

# if operating system is windows
if os.name == 'nt':
    alphaMELTS = AlphaMELTS(
        alphamelts_path=r"C:\Users\Scott\OneDrive\Desktop\alphaMELTS2-master\alphaMELTS2-master",
        perl_path=r"C:\Users\Scott\OneDrive\Desktop\alphaMELTS2-master\alphaMELTS2-master\strawberry-perl-5.32.1.1-64bit-portable\perl\bin\perl.exe"
    )
else:
    alphaMELTS = AlphaMELTS(
        alphamelts_path="/Users/scotthull/Documents - Scott’s MacBook Pro/alphaMELTS2-master"
    )

# save current working directory
cwd = os.getcwd()
# change working directory to alphamelts package or else it won't work
os.chdir(alphaMELTS.alphamelts_package_path)

# =================== WRITE THE MELTS FILES ===================

bsp_file = alphaMELTS.write_environment_file(
    settings={
        "ALPHAMELTS_CALC_MODE": "MELTS",
        "ALPHAMELTS_VERSION": "MELTS",
        "ALPHAMELTS_MODE": "isobaric",
        "ALPHAMELTS_MAXT": 3000,
        "ALPHAMELTS_DELTAT": delta_T,
        "ALPHAMELTS_MINT": 1020,
        "ALPHAMELTS_FRACTIONATE_SOLIDS": "true",
        "ALPHAMELTS_SAVE_ALL": "true",
        "ALPHAMELTS_SKIP_FAILURE": "true",
        "Suppress": "alloy-liquid"
    },
    fname="bsp_env_file.txt"
)

BULK_EARTH.write_melts_file(title=title, settings=bsp_settings, path=alphaMELTS.alphamelts_package_path)

# =================== DEFINE MELTS COMMANDS ===================

# format alphaMELTS commands
commands = []
# read in the melts file
commands += [1, title + ".melts"]
# set fO2
commands += [5, fO2_buffer, 7, fO2_offset, 'x']
# suppress alloy-liquid
commands += [8, 'alloy-liquid', 0, 'x']
# execute
commands += [4, 1, 0]

# =================== RUN ALPHAMELTS ===================

# alphaMELTS.run_alphamelts(
#     commands=commands,
#     env_file_path=bsp_file,
# )

# change back to original working directory
os.chdir(cwd)
