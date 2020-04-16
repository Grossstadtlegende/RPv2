__author__ = 'Mike'
from RPv2 import verbous
import numpy as np
import experiments, measurements


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
        self.experiments = None
        self.measurements = []
        self.treatments = None
        self.composition = None

    def add_experiment(self, variety=None):
        implemented = {'TreatmentPint': experiments.TreatmentPint,
                       'TreatmentAF': experiments.TreatmentAF}
        exp = implemented[variety]()
        self.experiments.append(exp)

    def add_measurement(self, variety=None):
        implemented = {'irm':measurements.IRM}

        if variety.lower() in implemented:
            m = implemented[variety.lower()]()
            self.measurements.append(m)

    def add_composition(self, composition, mixture, mill_protocol, mill_time):
        self.composition = composition
        self.ni = int(composition[-3:])
        self.fe = 100 - self.ni
        self.mixture = mixture
        self.mill_protocol = mill_protocol
        self.mill_time = int(mill_time)
        verbous.ADD('<< %s >> Composition: Fe%iNi%i %s %s %i' %(self.name, self.fe, self.ni, self.mixture, self.mill_protocol, self.mill_time))
    def __str__(self):
        out = verbous.INFO('<< Sample >> %s %.1f' %(self.name, self.mass), out=True)
        return out

    def infos(self):
        verbous.line()
        verbous.INFO('SAMPLE \t %s' %self.name)
        verbous.line()
        print '\t Mass: \t\t\t %.1f' %self.mass
        if self.composition != None:
            print '\t Composition: \t Fe%iNi%i' %(self.fe, self.ni)
            print '\t Mixture: \t\t %s' %(self.mixture)
            print '\t Mill Protocoll: %s' %(self.mill_protocol)
            print '\t Mill time: \t %s' %(self.mill_time)
        if self.experiments:
            for i in experiments:
                verbous.line()
                i.info()
        if self.measurements:
            for i in measurements:
                verbous.line()
                i.info()
        print