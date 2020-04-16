# coding=utf-8
__author__ = 'Mike'

from RPv2 import verbous
import experiments, measurements, infos, data
from RPv2 import machines
import numpy as np
from math import degrees
import matplotlib.pyplot as plt
from pprint import pprint
import scipy as sp


class Measurement(object):
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
        sample = self.sample
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
        self.sample = sample

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

        if step not in ['th', 'pt', 'ptrm', 'ac', 'ck', 'tr', 'sum']:
            verbous.WARNING('%s not found' % step)
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

    def __init__(self, file, treatment, machine, sample=None, *args, **kwargs):
        self.steplist = kwargs.get('steplist')
        Measurement.__init__(self, file, treatment, machine, sample)
        self.ptrm = None
        self.sum = None
        verbous.NEW('|- Paleointensity')

    def calc_ptrm(self):
        self.ptrm = [[self.th[i][0],
                      self.th[i][1] - self.pt[i][1], self.th[i][2] - self.pt[i][2], self.th[i][3] - self.pt[i][3]]
                     for i in range(len(self.th)) for j in range(len(self.pt)) if self.th[i][0] == self.pt[j][0]]
        self.ptrm = np.array(self.ptrm)

    def calc_sum(self):
        if not self.ptrm == None:
            self.calc_ptrm()
        self.sum = [[self.th[i][0],
                     self.th[i][1] + abs(self.ptrm[i][1]), self.th[i][2] + abs(self.ptrm[i][2]),
                     self.th[i][3] + abs(self.ptrm[i][3])]
                    for i in range(len(self.th)) for j in range(len(self.ptrm)) if self.th[i][0] == self.ptrm[j][0]]
        self.sum = np.array(self.sum)

    def import_pint_data(self, *args, **kwargs):
        verbous.IMPORTING('PalInt ')
        self.import_data()
        steps = ['th', 'pt', 'ck', 'ac', 'tr']

        for step in steps:
            steps_list = self.steplist[step]

            # search for index of rawdata with run_nr = run_nr from list
            run_idx = [i for i in range(len(self._raw_data['run'][0])) if
                       self._raw_data['run'][0][i] in steps_list[:, 0]]

            # search for index of rawdata with af_treatment = specified
            af_idx = [i for i in range(len(self._raw_data['par1'][0])) if
                      self._raw_data['par1'][0][
                          i] == self.treatment.AF]

            #todo figure out why it is wrong!
            # idx contained in both
            idx = sorted(list(set(run_idx) & set(af_idx)))
            if len(self.steplist[step]) != len(idx):
                runs_idx = [self.steplist[step][idx.index(i), 0] for i in idx]
                runs_difference = list(set(self.steplist[step][:, 0]).difference(set(runs_idx)))
                # for i in range(len(runs_difference)):
                # verbous.WARNING('step << %s %s >> number problem with runs << %s >>' %(self.steplist[], step.upper(), runs_difference[i]) )

            A = list(self._raw_data['run'][0])
            B = list(self.steplist[step][:, 0])
            # print step
            # print(self.steplist[step])
            data = [[self.steplist[step][idx.index(i), 1],
                     self._raw_data['x'][0][i], self._raw_data['y'][0][i], self._raw_data['z'][0][i]] for i in idx]
            self.__dict__.update({step: np.array(data)})

        self.pt = np.vstack((self.th[0], self.pt))
        self.calc_ptrm()
        self.calc_sum()

    def _getvalue(self, step, **kwargs):
        step = step.lower()
        norm = kwargs.get('norm')
        quantities = {'temp': getattr(self, step)[:, 0],
                      'x': getattr(self, step)[:, 1],
                      'y': np.array(getattr(self, step)[:, 2], dtype=np.ndarray),
                      'z': np.array(getattr(self, step)[:, 3], dtype=np.ndarray),
                      # 'sm': np.array(getattr(self, step)[:, 4], dtype=np.ndarray),
                      # 'time': np.array(getattr(self, step)[:, 5], dtype=np.ndarray),
                      'm': self.__get_M(step=step),
                      'd': self.__get_D(step=step),
                      'i': self.__get_I(step=step)}
        if norm:
            for q in ['x', 'y', 'z', 'm']:
                quantities[q] /= max(quantities[q])

        return quantities

    def plot(self, method='dunlop', quantity='m', *args, **kwargs):

        # implemented = {'dunlop': self.plot.dunlop}

        # def dunlop(self, quantity='m', *args, **kwargs):
        verbous.PLOTTING('dunlop plot << %s >>' % self.sample)

        if method == 'dunlop':
            for step in ['th', 'ptrm', 'sum']:
                x = self._getvalue(step, norm=False)['temp']
                y = self._getvalue(step, norm=False)[quantity]
                plot = plt.plot(x, y)
        if method == 'arai':
            x = self._getvalue('ptrm', norm=False)[quantity]
            y = self._getvalue('th', norm=False)[quantity]
            plot = plt.plot(x, y, 'o')
        if 'plt' in kwargs:
            plt.show()
            # implemented[method](quantity, args, kwargs)


class Hysteresis(Measurement):
    def __init__(self, treatment, machine, sample):
        Measurement.__init__(self, file=None, treatment=treatment, machine=machine, sample=sample)
        self.df = None
        self.uf = None
        self.virgin = None

    def import_data(self, files):
        for i in files:
            if self.sample.name in i:
                verbous.IMPORTING('%s ' % i)
                implemented = {'vsm': machines.vsm(i)}
                if self.machine in implemented:
                    self.segments, self._raw_data = implemented[self.machine]
                    for i in self.segments:
                        if abs(i[2]) == abs(i[4]):
                            if i[2] > i[4]:
                                self.df = np.array(self._raw_data[self.segments.index(i)])
                                verbous.ADD('DOWNFIELD branch of HYSTERESIS')
                            else:
                                self.uf = np.array(self._raw_data[self.segments.index(i)])
                                verbous.ADD('UPFIELD branch of HYSTERESIS')
                        else:
                            self.virgin = np.array(self._raw_data[self.segments.index(i)])
                            verbous.ADD('VIRGIN branch of HYSTERESIS')

    def normalize(self, value='mass'):
        verbous.INFO('NORMALIZING data to sample mass')
        factor = 1
        if value == 'mass':
            factor = self.sample.mass
        if value == 'max':
            factor = max(self.df[:, 1])
        try:
            self.df[:, 1] /= factor
            self.uf[:, 1] /= factor
        except:
            verbous.ERROR('NO DOWN/UPFIELD branches')
        try:
            self.virgin[:, 1] /= factor
        except TypeError:
            pass

    def plot(self, plot=None, show=False):
        if not plot:
            ax = plt.subplot(1, 1, 1)
            ax.set_xlabel('Field [T]')
            ax.set_ylabel('moment [Am^2/mg]')
            ax.plot([0, 0], [-1, 1], '--', color='grey')
            ax.plot([-1, 1], [0, 0], '--', color='grey')
            # handles, labels = ax.get_legend_handles_labels()
        else:
            ax = plot
        X = np.concatenate((self.df[:, 0], self.uf[:, 0]), axis=0)
        Y = np.concatenate((self.df[:, 1], self.uf[:, 1]), axis=0)
        plot = ax.plot(X, Y, label=self.treatment.get_label('m_time'))
        ax.set_ylim(-max(self.df[:, 1]) * 1.1, max(self.df[:, 1]) * 1.1)
        ax.set_xlim(-max(self.df[:, 0]) * 1.1, max(self.df[:, 0]) * 1.1)
        # if not plot:

        if show:
            ax.legend(handles, labels)
            plt.show()
        else:
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles, labels, loc='best')
            return plot


class Simple_Moment(Measurement):
    def __init__(self, treatment, machine, sample):
        # super(Measurement).__init__()
        super(IRM, self).__init__(self, treatment=treatment, machine=machine, sample=sample)
        self.type = 'irm'


class IRM(Measurement):
    def __init__(self, treatment, machine, sample):
        # super(Measurement).__init__()
        super(IRM, self).__init__(self, treatment=treatment, machine=machine, sample=sample)
        self.type = 'irm'

    def import_data(self, files):
        for i in files:
            if self.sample.name in i:
                verbous.IMPORTING('%s ' % i)
                implemented = {'vsm': machines.vsm(i)}
                if self.machine in implemented:
                    self.segments, self._raw_data = implemented[self.machine]
                    self.irm = np.array(self._raw_data[0])
                    self.bf = np.array([[-i[0], i[1], i[2]] for i in self._raw_data[1]])

                    x_irm = np.linspace(min(self.irm[:, 0]), max(self.irm[:, 0]), 1000)
                    irm_rem_interpolated = sp.interpolate.pchip_interpolate(self.irm[:, 0], self.irm[:, 1], x_irm)
                    irm_interpolated = sp.interpolate.pchip_interpolate(self.irm[:, 0], self.irm[:, 2], x_irm)

                    x_bf = np.linspace(min(self.bf[:, 0]), max(self.bf[:, 0]), 1000)
                    bf_rem_interpolated = sp.interpolate.pchip_interpolate(self.bf[:, 0], self.bf[:, 1], x_bf)
                    bf_interpolated = sp.interpolate.pchip_interpolate(self.bf[:, 0], self.bf[:, 2], x_bf)

                    # self.bf_int =
                    # 0 = field, 1 = remanence 2 = induced
                    # plt.plot(x_irm, irm_rem_interpolated/max(irm_rem_interpolated))
                    # plt.plot(self.irm[:,0], self.irm[:,1]/max(self.irm[:,1]), '--')

                    test = -(self.bf[:, 1] / max(self.irm[:, 1]) - ( 1 - 2 * self.irm[:, 1] / max(self.irm[:, 1])))
                    energy = [sum(test[:i]) for i in range(len(test))][-1]
                    print energy

                    ''' HENKEL PLOT '''
                    plt.plot(self.irm[:, 1] / max(self.irm[:, 1]), self.bf[:, 1] / max(self.irm[:, 1]))
                    plt.plot(self.irm[:, 1] / max(self.irm[:, 1]), 1 - 2 * self.irm[:, 1] / max(self.irm[:, 1]), '--',
                             color='grey')
                    plt.fill_between(
                        self.irm[:, 1] / max(self.irm[:, 1]),
                        self.bf[:, 1] / max(self.irm[:, 1]),
                        1 - 2 * self.irm[:, 1] / max(self.irm[:, 1]),
                        # self.irm[:, 1] / max(self.irm[:, 1]),
                        alpha=0.5,
                        color='grey'
                    )
                    plt.ylim([-1.1, 1.1])


                    # plt.plot(x_irm, irm_interpolated)
                    # plt.plot(x_bf, bf_rem_interpolated/max(irm_rem_interpolated))
                    # plt.plot(self.bf[:,0], self.bf[:,1]/max(self.bf[:,1]), '--')
                    # plt.plot(x_bf, bf_interpolated)
                    plt.show()