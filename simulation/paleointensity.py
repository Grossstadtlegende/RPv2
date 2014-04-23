# -*- coding: utf-8 -*-

__author__ = 'Mike'
import verbous
from lmfit import Parameters
import numpy as np
import fit.distributions
import matplotlib.pyplot as plt
import copy

def get_data(parameters, *args, **kwargs):
    if 'info' in kwargs:
        pass

    '''
    amp: amplitude of function
    center: mean of function - called 'center' in parameters
    standard deviation:
    variance:
    skewness:
    '''

    verbous.INFO('generating data with:')
    for i in parameters:
        verbous.INFO('\t %s' % parameters[i])

    temps = np.linspace(20, 700, 681)

    parameters_th = copy.deepcopy(parameters)
    parameters_ptrm = Parameters()

    ### TH steps
    y = fit.distributions.normal_skew(temps, parameters_th, dfunc='cdf', check=False)
    th = (1- y/max(y))
    ### pTRM steps
    for p in parameters:
        if 'delta' in p:
            parameters_ptrm.add(p[6:], value=parameters_th[p[6:]].value+parameters_th[p].value)
        else:
            parameters_ptrm.add(p, value=parameters_th[p].value)

    pt = fit.distributions.normal_skew(temps, parameters_ptrm, dfunc='cdf', check=False)
    pt /= max(pt)
    # print len(temps), len(y), len(y2)
    plt.subplot(2, 1, 1)
    plt.plot(temps, th, '-')
    plt.plot(temps, pt, '-')
    plt.title('PSD simulation')
    plt.ylabel('Moment normalized')

    plt.subplot(2, 1, 2)
    plt.plot(th, pt, 'r-')
    plt.xlabel('pTRM gained')
    plt.ylabel('NRM remaining')

    plt.show()
    verbous.RUNTIME()