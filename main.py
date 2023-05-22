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

bsp_settings = {
    'Increment Temperature': -5,
    'Initial Pressure': 500,
    'Final Pressure': 500,
    'dp/dt': 0,
    'Mode': "Fractionate Solids",
}

alphaMELTS = AlphaMELTS(r"C:\Users\Scott\OneDrive\Desktop\alphaMELTS2-master\alphaMELTS2-master")
bsp_file = alphaMELTS.write_environment_file(
    settings={
        "ALPHAMELTS_VERSION": "pMELTS",
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

BULK_EARTH.write_melts_file(title="earth", settings=bsp_settings, path=alphaMELTS.alphamelts_package_path)
