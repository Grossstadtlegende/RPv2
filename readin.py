import csv
import numpy as np
import verbous

def sample_masses(file):
    header = [str, str, str]
    reader_object = csv.reader(open(file, 'rU'), delimiter=',')
    aux = [i for i in reader_object]
    header = aux[0]
    data = aux[1:]
    return header, data


def steplist(file):
    header = [int, int, str]
    reader_object = csv.reader(open(file, 'rU'), delimiter='\t')
    out = [i for i in reader_object][1:]
    run = [int(i[0]) for i in out]
    temp = [int(i[1]) for i in out]
    step = [i[2].lower() for i in out]

    out = {i: np.array([[int(run[j]), int(temp[j])] for j in range(len(out)) if step[j] == i]) for i in list(set(step))}
    return out


def get_data(file, header, column_name, header_skip):
    '''
    help function
    '''
    reader_object = csv.reader(open(file, 'rU'), delimiter='\t')
    for i in range(header_skip):
        reader_object.next()
    out = [line[header[column_name][0]] for line in reader_object]
    for i in range(len(out)):
        if out[i] == 'None':
            out[i] = 0.
    try:
        out = map(header[column_name][1], out)
    except ValueError:
        verbous.ERROR(column_name)
    return np.array(out[header_skip:])
