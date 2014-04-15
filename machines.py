import readin
import datetime
import numpy as np
import datetime
import csv
import datetime
def SushiBar(file):
    header = {
        'sample': [0, str], 'site': [1, str], 'type': [2, str], 'run': [3, int], 'time': [4, str],
        'x': [5, float], 'y': [6, float], 'z': [7, float],
        'M': [8, float], 'Dc': [9, float], 'Ic': [10, float], 'Dg': [11, float], 'Ig': [12, float],
        'Ds': [13, float], 'Is': [14, float], 'a95': [15, float], 'sM': [16, float],
        'npos': [17, float], 'Dspin': [18, float], 'Ispin': [19, float], #'holder/sample': [20, float],
        #'cup/sample': [21, float],
        'bl diff/sample': [22, float], #'steps/rev': [23, float],
        'par1': [24, float], 'par2': [25, float], 'par3': [26, float], 'par4': [27, float],
        'par5': [28, float], 'par6': [29, float], 'strat_level': [30, float], 'geoaz': [31, float],
        'hade': [32, float], 'dipdir': [33, float], 'dip': [34, float]
    }
    reader_object = csv.reader(open(file, 'rU'), delimiter='\t')
    aux = [i for i in reader_object][1:]
    for i in range(len(aux)):
        for j in range(len(aux[i])):
            if aux[i][j] == 'None':
                aux[i][j] = 0

    out = {column.lower(): np.array([header[column][1](i[header[column][0]]) for i in aux]) for column in header}
    #todo time

    # for i in out['time']:
    #     print
    #     print i[:19]
    #     print datetime.datetime.strptime(i[:19], "%Y-%M-%d %H:%M:%S:")

    return out

def CryoNL(file):
    header = {
        'sample': [0, str], 'coreaz': [1, float], 'coredip': [2, float], 'bedaz': [3, float], 'beddip': [4, float],
        'vol': [5, float], 'weight': [6, float], 'step': [7, str],
        'type': [8, str], 'comment': [9, str], 'time': [10, str], 'mode': [11, str], 'x': [12, float], 'y': [13, float],
        'z': [14, float], 'M': [15, float],
        'sm': [16, float], 'a95': [17, float], 'dc': [18, float], 'ic': [19, float], 'dg': [20, float],
        'ig': [21, float],
        'ds': [22, float], 'is': [23, float],
    }
    out = {column.lower(): readin.get_data(file, header, column, header_skip=2) for column in header}
    return out