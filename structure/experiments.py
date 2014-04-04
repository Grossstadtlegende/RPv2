import verbous
import experiments, measurements, infos, data
import time
import copy
import numpy as np
import matplotlib.pyplot as plt



class Experiment():
    def __init__(self, parameters):
        verbous.NEW('Experiment')
        self.__errcounter = 0
        self.__dict__.update(parameters)
        self.measurements = []


    def get_treatments(self):
        for i in self.measurements:
            print i.treatment.__dict__.keys()

    def find_treatment(self, attr):
        for i in self.measurements:
            for key in attr:
                if key in i.treatment.__dict__.keys():
                    if attr[key] == getattr(i.treatment, key):
                        return i


class TreatmentAF(Experiment):
    def add_measurement(self, file, treatment=None):
        verbous.ADD('Measurement')
        measurement = measurements.AFdemag(file, treatment)
        measurement.import_af_data()
        self.measurements.append(measurement)

    def difference(self, base):
        verbous.CALC('Difference %s' %base)
        base = self.find_treatment({'P': 0})
        calculations = ['x', 'y', 'z', 'm']
        self.differences = []
        for i in self.measurements:
            if not i == base:
                aux = copy.deepcopy(i)
                aux2 = copy.deepcopy(i)
                for n in calculations:
                    aux.__dict__[n] = np.array(getattr(aux, n))- np.array(getattr(base, n))
                # aux._update_data()
                # aux.m = aux._get_M()
                aux.info = {'difference':base}
                self.differences.append(aux)

    def make_pdf(self, x='field', y='m', *args, **kwargs):
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
        if 'differences' not in self.__dict__.keys():
            self.difference(base = {P:0})
        for d in self.differences:
            X = getattr(d, x)
            Y = getattr(d, y)
            ax2.plot(X, Y,
                    linestyle='-',
                    # color='#111111',
                    label='d'+m.treatment.get_label(),
            )

        ax2.set_xlabel(x)
        ax.set_ylabel(y)
        ax.ticklabel_format(axis='y', style='sci', scilimits=(-1,1))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)
        plt.show()