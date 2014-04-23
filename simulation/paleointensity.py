__author__ = 'Mike'
import verbous
from lmfit import Parameters
import numpy as np
import fit.distributions
import matplotlib.pyplot as plt

def get_data(parameters, *args, **kwargs):
    if 'info' in kwargs:
        pass

    '''
    amp: amplitude of function
    center: mean of function - called 'center' in parameters
    standard deviation:
    variance:
    skewness:
    kurtosis:
    '''

    verbous.INFO('generating data with:')
    for i in parameters:
        verbous.INFO('\t %s' %parameters[i])
    temps = np.linspace(20, 700, 681)
    dist = fit.distributions.skewed_gauss(x=temps, parameters=parameters)
    y = dist.y
    y2 = dist.cdf()
    plt.plot(temps, y)
    plt.semilogx()
    # plt.plot(temps, y2)
    plt.show()
    verbous.RUNTIME()