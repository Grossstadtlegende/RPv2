import readin
import datetime
import numpy as np
def SushiBar(file):
    header = {
        'sample': 0, 'site': 1, 'type': 2, 'run': 3, 'time': 4, 'x': 5, 'y': 6, 'z': 7,
        'M': 8, 'Dc': 9, 'Ic': 10, 'Dg': 11, 'Ig': 12, 'Ds': 13, 'Is': 14, 'a95': 15,
        'sM': 16, 'npos': 17, 'Dspin': 18, 'Ispin': 19, 'holder/sample': 20, 'cup/sample': 21,
        'bl diff/sample': 22, 'steps/rev': 23, 'par1': 24, 'par2': 25, 'par3': 26, 'par4': 27,
        'par5': 28, 'par6': 29, 'strat_level': 30, 'geoaz': 31, 'hade': 32, 'dipdir': 33,
        'dip': 34, 'mode': 1, 'step': 25, 'type': 24
    }
    dtyp = {
        'sample': str, 'site': str, 'type': str, 'run': int, 'time': str,
        'x': float, 'y': float, 'z': float,
        'm': float, 'dc': float, 'ic': float, 'dg': float, 'ig': float, 'ds': float, 'is': float, 'a95': float,
        'sm': float, 'npos': float, 'dspin': float, 'ispin': float, 'holder/sample': float, 'cup/sample': float,
        'bl diff/sample': float, 'steps/rev': float, 'par1': float, 'par2': float, 'par3': float, 'par4': float,
        'par5': float, 'par6': float, 'strat_level': float, 'geoaz': float, 'hade': float, 'dipdir': float,
        'dip': float, 'headerskip': str, 'mode': str, 'step': str, 'type': str
    }
    out = {column.lower(): readin.get_data(file, header, column, header_skip=1) for column in header}
    for i in out:
        out[i] = map(dtyp[i], out[i])
    return out