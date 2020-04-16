# -*- coding: utf-8 -*-

__author__ = 'Mike'
import verbous
from lmfit import Parameters, minimize
import numpy as np
from fit import fitting, distributions
import matplotlib.pyplot as plt
import copy
from mpltools import style

style.use('ggplot')


def get_data(parameters=None, data_th=None, data_ptrm=None, check=False, *args, **kwargs):
    if 'info' in kwargs:
        pass

    '''
    amp: amplitude of function
    center: mean of function - called 'center' in parameters
    standard deviation:
    variance:
    skewness:
    '''
    parameters_ptrm = None
    parameters_th = None

    if parameters == None and data_th == None:
        verbous.ERROR('Neither parameters not data for fit defined')

    temps = np.linspace(20, 700, 681)

    if data_th != None:
        th_fit, parameters_th = fitting.normal_skewed(data_th[:, 0], data_th[:, 1])

    if data_ptrm != None:
        ptrm_fit, parameters_ptrm = fitting.normal_skewed(data_ptrm[:, 0], data_ptrm[:, 1])

    if parameters_th == None:
        parameters_th = copy.deepcopy(parameters)
    if parameters_ptrm == None:
        parameters_ptrm = Parameters()

    ### TH steps
    verbous.INFO('GENERATING << TH >> data with:')
    for i in parameters_th:
        verbous.INFO('\t %s' % parameters_th[i])

    ''' GENERATING TH CATALOGUE '''
    th = distributions.normal_skew(temps, parameters_th, dfunc='cdf', check=False)
    th_dist = distributions.normal_skew(temps, parameters_th, dfunc='pdf', check=False)
    th = (1 - th / max(th))

    ''' GENERATING PTRM CATALOGUE '''
    ### pTRM steps
    if data_ptrm == None:
        for p in parameters:
            if 'delta' in p:
                parameters_ptrm.add(p[6:], value=parameters_th[p[6:]].value + parameters[p].value)
            else:
                parameters_ptrm.add(p, value=parameters_th[p].value)
    verbous.INFO('GENERATING << pTRM >> data with:')
    for i in parameters_ptrm:
        verbous.INFO('\t %s' % parameters_ptrm[i])
    pt = distributions.normal_skew(temps, parameters_ptrm, dfunc='cdf', check=False)
    pt_dist = distributions.normal_skew(temps, parameters_ptrm, dfunc='pdf', check=False)
    pt /= max(pt)

    # print len(temps), len(y), len(y2)
    fig, (ax, ax1) = plt.subplots(2, 1)
    ax.plot(temps, th, 'g-')
    ax.plot(temps, pt, 'b-')
    ax.plot(temps, th + pt, 'r--')

    if data_th != None:
        ax.plot(data_th[:, 0], data_th[:, 1], 'g.',
                alpha=0.3)
        ax.plot(data_ptrm[:, 0], data_ptrm[:, 1], 'b.',
                alpha=0.3)
    ax.fill_between(temps, 0, pt_dist/max(pt_dist),
                    color='b',
                    alpha=0.2)
    ax.fill_between(temps, 0, th_dist/max(th_dist),
                    color='g',
                    alpha=0.2)

    ax.set_title('PSD simulation')
    ax.set_ylabel('Moment normalized')
    ax.set_ylim([-0.01, max(th) * 1.1])

    ax1.plot(th, pt, 'r-')
    ax1.plot([1, 0], [0, 1], '--')
    ax1.set_xlabel('pTRM gained')
    ax1.set_ylabel('NRM remaining')

    plt.show()
    verbous.RUNTIME()