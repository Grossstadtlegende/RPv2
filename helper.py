def diff(x, y, smoothing=1):
    '''
    
    '''

    aux = [
        [x[i], (y[i - smoothing] - y[i + smoothing]) / (x[i - smoothing] - x[i + smoothing])]
        for i in
        range(smoothing, len(x) - smoothing)]

    out = np.array(aux)
    return out
