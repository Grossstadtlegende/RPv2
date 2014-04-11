__author__ = 'Mike'
import verbous
import numpy as np
import experiments


class Project():
    '''

    '''

    ''' INFO '''

    def print_implemented_experiments(self):
        verbous.INFO('implemented so far:\t %s' % self.implemented_exp)

    def __init__(self):
        self.samples = []
        self.experiments = []
        self.measurements = []
        self.treatments = []
        self.implemented_exp = ['TreatmentPint', 'TreatmentAF']


    ''' find '''
    def find_sample(self, sample_name):
        for sample in self.samples:
            if sample.name == sample_name:
                return sample


    ''' add '''

    def add_sample(self, sample):
        self.samples.append(sample)

    def add_many_samples(self, sample_list, masses_list=None):
        for i in range(len(sample_list)):
            if masses_list != None or masses_list == []:
                if len(sample_list) != len(masses_list):
                    verbous.ERROR('sample / mass list length does not match, ignoring masses')
                    masses_list = np.ones(len(sample_list))
            else:
                masses_list = np.ones(len(sample_list))
            self.samples.append(Sample(name=sample_list[i], mass=masses_list[i]))

    def add_experiment(self, variety=None, sample=None):
        if not variety:
            verbous.ERROR('please specify experiment variety')
            self.print_implemented_experiments()
        if variety:
            if variety not in self.implemented_exp:
                verbous.ERROR('experiment variety << %s >> not implemented' % variety)
                self.print_implemented_experiments()
            else:
                try:
                    sample = self.find_sample(sample)
                    sample.add_experiment(variety=variety)
                except AttributeError:
                    verbous.ERROR('sample: << %s >> could not be found' %sample)

    ''' get '''

    def get_sample_names(self):
        out = [str(i.name) for i in self.samples]
        return out

class Sample():
    def __init__(self, name, mass=1):
        self.name = name
        self.mass = mass
        self.experiments = []

    def add_experiment(self, variety=None):
        implemented = {'TreatmentPint': experiments.TreatmentPint,
                       'TreatmentAF': experiments.TreatmentAF}
        exp = implemented[variety]()
        self.experiments.append(exp)