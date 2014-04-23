__author__ = 'Mike'
from RockPy import fitting

__author__ = 'Mike'
import numpy as np
from scipy.special import erf, erfc
import matplotlib.pyplot as plt
from scipy import pi, sqrt, exp
import scipy.integrate

def normal(x, parameters, dfunc='pdf', *args, **kwargs):
    '''
    parameters:
        amp: amplitude of function
        mean: mean of function - called 'center' in parameters
        standard deviation:
        variance:
        skewness:
        kurtosis:

    :option:
        output:
            pdf [standard] gives probability density function
            cdf

    :math:
       e^(-(x-mu)^2/(2 sigma^2))/(sqrt(2 pi) sigma)

    '''

    amp = parameters['amp'].value
    center = parameters['center'].value
    sig = parameters['sig'].value
    print amp, center, sig

    if dfunc == 'pdf':
        out_pdf = np.exp(-(x - center) ** 2 / 2 * sig ** 2) / np.sqrt(2 * np.pi) * sig
        out_pdf *= amp / max(out_pdf)
        return out_pdf
    if dfunc == 'cdf':
        out_cdf = amp * 0.5 * erfc((center - x) / np.sqrt(2) * sig)
        return out_cdf


def normal_skew(x, parameters, dfunc='pdf', check=False, *args, **kwargs):
    '''
    parameters:
        amp: amplitude of function
        mean: mean of function - called 'center' in parameters
        standard deviation:
        variance:
        skewness:
        kurtosis:

    :option:
        output:
            pdf [standard] gives probability density function
            cdf

    :math:
        (e^(-(x-mu)^2/(2 sigma^2)) erfc(-(alpha (x-mu))/(sqrt(2) sigma)))/(sqrt(2 pi) sigma)
    '''

    amp = parameters['amp'].value
    center = parameters['center'].value
    sig = parameters['sig'].value
    skew = parameters['skew'].value

    out_pdf = np.exp(-(x - center) ** 2 / 2 * sig ** 2) * erfc(-(skew * (x - center)) / (np.sqrt(2) * sig)) / (
    np.sqrt(2 * np.pi) * center)
    out_pdf *= amp / max(out_pdf)
    out_cdf = amp * 0.5 * erfc((center - x) / np.sqrt(2) * sig)

    if check:
        # plt.plot(x, out_pdf)
        plt.plot(x, out_cdf)
        plt.show()

    if dfunc == 'pdf':
        return out_pdf
    if dfunc == 'cdf':
        return out_cdf


# class skewed_gauss():
#     def __pdf(self, t):
#         return 1 / sqrt(2 * pi) * exp(-t ** 2 / 2)
#
#     def __cdf(self, t):
#         return (1 + erf((self.skew * t) / sqrt(2))) / 2
#
#     def __init__(self, x, parameters):
#         self.x = x
#         self.x_fine = np.linspace(min(x), max(x), 10)
#
#         self.parameters = parameters
#
#         self.amp = self.parameters['amp'].value
#         self.center = self.parameters['center'].value
#         self.sig = self.parameters['sig'].value
#         self.skew = self.parameters['skew'].value
#
#         self.t = (self.x - self.center) / self.sig
#         self.t_fine = (self.x - self.center) / self.sig
#
#         self.y = 2 / self.sig * self.__pdf(self.t) * self.__cdf(self.t)
#         self.y_fine = 2 / self.sig * self.__pdf(self.t_fine) * self.__cdf(self.t_fine)
#
#     def cdf(self):
#         aux = [[self.x_fine[i], scipy.integrate.simps(self.y_fine[:i])] for i in range(len(self.y_fine)+1)]
#         print aux
#         return aux

def skewed(x, sigmag, mu, alpha, c, a):
    #normal distribution
    normpdf = (1 / (sigmag * np.sqrt(2 * math.pi))) * np.exp(-(np.power((x - mu), 2) / (2 * np.power(sigmag, 2))))
    normcdf = (0.5 * (1 + sp.erf((alpha * ((x - mu) / sigmag)) / (np.sqrt(2)))))
    return 2 * a * normpdf * normcdf + c
