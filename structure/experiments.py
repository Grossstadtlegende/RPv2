import verbous
import experiments, measurements, infos, data
import time
import copy
import numpy as np
import matplotlib.pyplot as plt
from mpltools import style
import scipy.interpolate
import matplotlib.mlab as ml
import machines
import readin

style.use('ggplot')


class Experiment():
    def __init__(self, sample, parameters={}):
        verbous.NEW('Experiment')
        self.__errcounter = 0
        self.__dict__.update(parameters)
        self.measurements = []
        self.differences = []
        self.derivatives = []

    def get_treatments(self, mode='measurements', *args, **kwargs):

        implemented = {'measurements': self.measurements,
                       'differences': self.differences,
                       'derivatives': self.derivatives}

        aux = [i.treatment.__dict__ for i in implemented[mode]]
        out = {}
        for i in aux:
            for key in i:
                if not key in out:
                    out[key] = []
                out[key].append(i[key])
        return out

    def find_treatment(self, attr, typ='measurements'):
        implemented = {'measurements': self.measurements,
                       'differences': self.differences,
                       'derivatives': self.derivatives}

        if attr:
            for i in implemented[typ]:
                for key in attr:
                    if key in i.treatment.__dict__.keys():
                        if attr[key] == getattr(i.treatment, key):
                            return i
        else:
            return self.measurements[0]


class TreatmentAF(Experiment):
    def add_measurement(self, file, treatment=None, sample=None):
        verbous.ADD('Measurement')
        measurement = measurements.AFdemag(file, treatment, machine='sushibar', sample=sample)
        measurement.import_af_data()
        self.measurements.append(measurement)

    def difference(self, base):
        verbous.CALC('Difference %s' % base)
        base = self.find_treatment(base)
        if not base:
            verbous.ERROR('base: %s not found' % base)
        calculations = ['x', 'y', 'z', 'm']
        self.differences = []
        for i in self.measurements:
            # if not i == base:
            aux = copy.deepcopy(i)
            for n in calculations:
                aux.__dict__[n] = np.array(getattr(aux, n)) - np.array(getattr(base, n))
            aux.info = {'difference': base}
            self.differences.append(aux)

    def derivative(self, *args, **kwargs):
        kwargs.get('smothing', 1)
        verbous.CALC('Derivatives')
        calculations = ['x', 'y', 'z', 'm']

        for i in self.measurements:
            aux = copy.deepcopy(i)
            for n in calculations:
                aux.__dict__[n] = np.array(getattr(aux, n)) - np.array(getattr(base, n))
            aux.info = {'derivatives': smothing}
            self.differences.append(aux)

    def do_nothing(self, *args, **kwargs):
        ''' routine does nothing '''
        pass

    def contour_treatment2(self, mode='data', ttype='P', base=None, options=None, *args, **kwargs):
        '''
        function make a contour plot with treatment data in x direction.

        '''
        implemented = {'measurements': self.do_nothing,
                       'differences': self.difference,
                       'derivatives': self.derivative}

        if mode in implemented:
            implemented[mode](base)
            treatments = self.get_treatments(typ=mode)
            print treatments
            fields = [self.find_treatment(attr={'P': i}, typ=mode).field for i in treatments['P']]
        else:
            verbous.ERROR('Mode not implemented -> no computation. Chose from: %s' % implemented.keys())
            # z = [self.find_treatment(attr={'P': i}, typ=typ).m for i in treatments['P']]
            #
            # y = np.array([i for i in treatments['P'] for j in range(len(fields[0]))])
            # fields = np.array([i for j in fields for i in j])
            # z = np.array([i for j in z for i in j])
            #
            # xi, yi = np.linspace(fields.min(), fields.max(), 100), np.linspace(y.min(), y.max(), 100)
            # xi, yi = np.meshgrid(xi, yi)
            # zi = scipy.interpolate.griddata((fields, y), z, (xi, yi), method='linear')
            # plt.contour(xi, yi, zi, 15, linewidths=0.5, colors='k')
            # plt.contourf(xi, yi, zi, 15, cmap=plt.cm.jet)
            # plt.colorbar()
            # plt.title('P-demagnetization [%s]' % typ)
            # plt.xlabel('af-field')
            # plt.ylabel('pressure')
            # plt.show()

    def contour_treatment(self, differences=None, options=None, *args, **kwargs):
        if differences:
            typ = 'differences'
            self.difference(base=differences)
        else:
            typ = 'measurements'

        treatments = self.get_treatments(typ=typ)
        fields = [self.find_treatment(attr={'P': i}, typ=typ).field for i in treatments['P']]
        z = [self.find_treatment(attr={'P': i}, typ=typ).m for i in treatments['P']]

        y = np.array([i for i in treatments['P'] for j in range(len(fields[0]))])
        fields = np.array([i for j in fields for i in j])
        z = np.array([i for j in z for i in j])

        xi, yi = np.linspace(fields.min(), fields.max(), 100), np.linspace(y.min(), y.max(), 100)
        xi, yi = np.meshgrid(xi, yi)
        zi = scipy.interpolate.griddata((fields, y), z, (xi, yi), method='linear')
        plt.contour(xi, yi, zi, 15, linewidths=0.5, colors='k')
        plt.contourf(xi, yi, zi, 15, cmap=plt.cm.jet)
        plt.colorbar()
        plt.title('P-demagnetization [%s]' % typ)
        plt.xlabel('af-field')
        plt.ylabel('pressure')
        plt.show()

    def data_vs_treatment(self, typ='measurements', q1='m', q2='field', *args, **kwargs):
        treatments = self.get_treatments(typ=typ)
        quant1 = [getattr(self.find_treatment(attr={'P': i}, typ=typ), q1) for i in treatments['P']]
        quant1 = [getattr(self.find_treatment(attr={'P': i}, typ=typ), q2) for i in treatments['P']]

        for i in treatments['P']:
            print treatments['P']

    def make_pdf(self, x='field', y='m', differences={'P': 0}, *args, **kwargs):
        ax = plt.subplot(2, 1, 1)
        ax2 = plt.subplot(2, 1, 2)
        for m in self.measurements:
            X = getattr(m, x)
            Y = getattr(m, y)
            ax.plot(X, Y,
                    linestyle='-',
                    # color='#111111',
                    label=m.treatment.get_label(),
            )
        self.difference(base=differences)
        for d in self.differences:
            X = getattr(d, x)
            Y = getattr(d, y)
            ax2.plot(X, Y,
                     linestyle='-',
                     # color='#111111',
                     label='d' + m.treatment.get_label(),
            )

        ax2.set_xlabel(x)
        ax.set_ylabel(y)
        ax.ticklabel_format(axis='y', style='sci', scilimits=(-1, 1))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)
        handles, labels = ax2.get_legend_handles_labels()
        ax2.legend(handles, labels)
        plt.show()


class TreatmentPint(Experiment):
    def __init__(self, sample, parameters={}):
        Experiment.__init__(self, sample, parameters)
        self.sample = sample
        verbous.NEW('|- Treatment vs. Paleointensity @ %s' % sample)

    def get_idx(self, attr, test):
        idx = [i for i in range(len(self._raw_data[attr])) if self._raw_data[attr][i] == test]
        return idx

    def import_data(self, machine=None):
        verbous.IMPORTING()
        implemented = {'SushiBar': machines.SushiBar,
                       'CryoNL': machines.CryoNL}
        self._raw_data = implemented[machine](self.file)
        self.treatments = list(sorted(set(self._raw_data['par1'])))
        self.samples = list(sorted(set(self._raw_data['sample'])))
        sample_idx = [np.where(self._raw_data['sample'] == sample)[0] for sample in
                      self.samples]  #indices of data of sample


    def add_measurement(self, file=None, treatment=None, machine=None, steplist=None):
        self.steplist = readin.steplist(steplist)
        verbous.ADD('Measurement << Paleointensity >>')
        measurement = measurements.PInt(file, treatment, machine, sample=self.sample, steplist=self.steplist)
        measurement.import_pint_data()
        self.measurements.append(measurement)