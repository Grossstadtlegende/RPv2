import numpy as np
import structure.experiments as exp
import verbous

file = 'test_data/AF_Palint.csv'
steplist = 'test_data/MUCSUSH-MANICOUAGAN DDC2-PalInt.steplist'

samples = ['DDC2-01x', 'DDC2-02x', 'DDC2-03x', 'DDC2-04x', 'DDC2-05x', 'DDC2-06x', 'DDC2-07x', 'DDC2-08x', 'DDC2-09',
           'DDC2-10', 'DDC2-11', 'DDC2-12', 'DDC2-13', 'DDC2-14', 'DDC2-15', 'DDC2-16', 'DDC2-17', 'DDC2-18', 'DDC2-19',
           'DDC2-20', 'DDC2-21', 'DDC2-22', 'DDC2-23', 'DDC2-24', 'DDC2-25', 'DDC2-26', 'DDC2-27', 'DDC2-28', 'DDC2-29',
           'DDC2-30', 'DDC2-31', 'DDC2-32', 'DDC2-33', 'DDC2-34', 'DDC2-35', 'DDC2-36', 'DDC2-37', 'DDC2-38', 'DDC2-39',
           'DDC2-40']

for sample in samples[17:18]:
    E = exp.TreatmentPint(sample=sample, parameters={'test':'test'})
    E.add_measurement(file=file, treatment={'AF':0}, machine='SushiBar', steplist=steplist)
    E.add_measurement(file=file, treatment={'AF':5}, machine='SushiBar', steplist=steplist)
    E.plot(plt=True, method='arai')
verbous.RUNTIME()
