import csv
import numpy as np

def get_data(file, header, column_name, header_skip):
    '''
    help function
    '''

    reader_object = csv.reader(open(file), delimiter='\t')
    strings = ['sample', 'site', 'type', ]
    datetime = ['time']
    out = np.array([line[header[column_name]] for line in reader_object])
    for i in range(len(out)):
        if out[i] == 'None':
            out[i] = 0
    return out[header_skip:]

