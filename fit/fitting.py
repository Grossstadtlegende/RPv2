__author__ = 'Mike'
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import math as math
import scipy.special as sp
import distributions

def skewed(x, y, *args, **kwargs):
    popt, pcov = curve_fit(distributions.skewed, x, y, p0=(1. / np.std(y), np.argmax(y), 0, 0, 1))

    y_fit = distributions.skewed(x, popt[0], popt[1], popt[2], popt[3], popt[4])

    plt.plot(x, yn)
    plt.plot(x, y_fit)
    plt.show()