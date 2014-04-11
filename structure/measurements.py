# coding=utf-8
__author__ = 'Mike'

import verbous
import experiments, measurements, infos, data
import machines
import numpy as np
from math import degrees
import matplotlib.pyplot as plt
from pprint import pprint


class Measurement():
    def _get_M(self):
        OUT = [np.sqrt(i[1] ** 2 + i[2] ** 2 + i[3] ** 2) for i in self.data]
        return np.array(OUT, dtype=np.ndarray)

    def _get_D(self):
        """
        :Parameter:
        :Return:
        """

        aux = [np.arctan2(i[2], i[1]) for i in self.data]
        D = map(degrees, aux)
        D = np.array(D)

        for i in range(len(D)):
            if D[i] < 0:
                D[i] += 360
            if D[i] > 360:
                D[i] -= 360
        return D

    def _get_I(self):
        """
        Calculates the Inclination from a given step.

        :Parameter: None
        :Return:
           I : inclination Data

        Inclination is calculated with,

        .. math::

           I = \\tan^{-1} \\left( \\sqrt{\\frac{z}{x^2 + y^2} } \\right)
        """
        aux = [np.arctan2(i[3], np.sqrt(i[2] ** 2 + i[1] ** 2)) for i in self.data]
        I = map(degrees, aux)
        I = np.array(I)

        return I

    def __init__(self, file, treatment, machine, sample):
        verbous.NEW('Measurement')
        self.file = file
        self.machine = machine.lower()
        self.sample = sample
        if treatment:
            verbous.ADD('Treatment')
            self.treatment = infos.Treatment(treatment)

    def get_diff(self, strength=1, *args, **kwargs):
        aux = [
            [self.x[i], (self.y[i - strength] - self.y[i + strength]) / (self.x[i - strength] - self.x[i + strength])]
            for i in
            range(strength, len(self.x) - strength)]

        out = np.array(aux)
        return out

    def import_data(self):
        verbous.IMPORTING()
        implemented = {'sushibar': machines.SushiBar,
                       'cryonl': machines.CryoNL}
        self._raw_data = implemented[self.machine](self.file)
        imported_samples = list(sorted(set(self._raw_data['sample'])))
        if self.sample not in imported_samples:
            verbous.ERROR('Sample << %s >> not in data file' % self.sample)
        else:
            if imported_samples > 1:
                idx = np.where(self._raw_data['sample'] == self.sample)
                for k in self._raw_data:
                    self._raw_data[k] = [self._raw_data[k][i] for i in idx]
        self.__dict__.update(self._raw_data)
        steps = ['th', 'pt', 'ck', 'ac', 'tr']

        for step in steps:
            steps_list = self.steplist[step]
            idx = [i for i in range(len(self._raw_data['run'][0])) if self._raw_data['run'][0][i] in steps_list[:, 0]]
            
    def get_attrib(self):
        print self.__dict__.keys()

    def plot(self, plot=None, x='field', y='m'):
        if not plot:
            ax = plt.subplot(1, 1, 1)
        X = getattr(m, x)
        Y = getattr(m, y)
        ax.plot(X, Y,
                linestyle='-',
                # color='#111111',
                label=m.treatment.get_label(),
        )
        if not plot:
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles, labels)
        plt.show()


class AFdemag(Measurement):
    def __init__(self, file, treatment, machine, sample):
        Measurement.__init__(self, file, treatment, machine, sample)
        verbous.NEW('|- AFdemag')

    def import_af_data(self):
        self.import_data()
        verbous.IMPORTING('AF ')
        self.data = np.array([self.par1, self.x, self.y, self.z]).T
        self.field = self.par1


class PInt(Measurement):
    def __init__(self, file, treatment, machine, sample=None, *args, **kwargs):
        self.steplist = kwargs.get('steplist')
        Measurement.__init__(self, file, treatment, machine, sample)
        verbous.NEW('|- Paleointensity')

    def import_pint_data(self):
        verbous.IMPORTING('PalInt ')
        self.import_data()

class PaleoInt(Measurement):
    '''
    OLD VERSION
    '''

    def _getvalue(self, step, **kwargs):
        step = step.lower()

        quantities = {'temp': getattr(self, step)[:, 0],
                      'X': getattr(self, step)[:, 1],
                      'Y': np.array(getattr(self, step)[:, 2], dtype=np.ndarray),
                      'Z': np.array(getattr(self, step)[:, 3], dtype=np.ndarray),
                      'sM': np.array(getattr(self, step)[:, 4], dtype=np.ndarray),
                      'time': np.array(getattr(self, step)[:, 5], dtype=np.ndarray),
                      'M': self.__get_M(step=step),
                      'D': self.__get_D(step=step),
                      'I': self.__get_I(step=step)}
        if 'norm' in kwargs:
            for q in ['X', 'Y', 'Z', 'M']:
                quantities[q] /= max(quantities[q])

        return quantities

    def __get_max(self, step, quantity):
        data = self._getvalue(step)[quantity]
        OUT = max([abs(i) for i in data])
        return OUT

    def __get_M(self, step='th'):
        implemented = {'th': self.th,
                       'pt': self.pt,
                       'ck': self.ck,
                       'ac': self.ac,
                       'tr': self.tr,
                       'ptrm': self.ptrm,
                       'sum': self.sum}
        OUT = [np.sqrt(i[1] ** 2 + i[2] ** 2 + i[3] ** 2) for i in implemented[step]]
        return np.array(OUT, dtype=np.ndarray)

    def __get_D(self, step='th'):
        """
        :Parameter:
           step : str [default = 'th']
                The paleomagnetic step
        :Return:

        """
        from math import degrees

        if step not in ['th', 'pt', 'ptrm', 'ac', 'ck', 'tr']:
            print 'No such step: %s' % step
            return

        implemented = {'th': self.th,
                       'pt': self.pt,
                       'ck': self.ck,
                       'ac': self.ac,
                       'tr': self.tr,
                       'ptrm': self.ptrm,
                       'sum': self.sum}

        aux = [np.arctan2(i[2], i[1]) for i in implemented[step]]
        D = map(degrees, aux)
        D = np.array(D)

        for i in range(len(D)):
            if D[i] < 0:
                D[i] += 360
            if D[i] > 360:
                D[i] -= 360
        return D

    def __get_I(self, step='th'):
        """
        Calculates the Inclination from a given step.

        :Parameter:
           step : str [default = 'th']
                The paleomagnetic step
        :Return:
           I : inclination Data

        Inclination is calculated with,

        .. math::

           I = \\tan^{-1} \\left( \\sqrt{\\frac{z}{x^2 + y^2} } \\right)
        """
        from math import degrees

        implemented = {'th': self.th,
                       'pt': self.pt,
                       'ck': self.ck,
                       'ac': self.ac,
                       'tr': self.tr,
                       'ptrm': self.ptrm,
                       'sum': self.sum}

        aux = [np.arctan2(i[3], np.sqrt(i[2] ** 2 + i[1] ** 2)) for i in implemented[step]]
        I = map(degrees, aux)
        I = np.array(I)

        return I