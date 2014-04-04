import structure.experiments as exp
import verbous
from pprint import pprint
import time
import numpy as np

test_file0 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P00.AF'
test_file1 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P11.AF'
test_file2 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P22.AF'
test_file3 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P33.AF'
test_file4 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P44.AF'
test_file5 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P55.AF'


A = exp.TreatmentAF(parameters={})
A.add_measurement(test_file0, treatment={'P_max': 0, 'P': 0})
A.add_measurement(test_file1, treatment={'P_max': 1, 'P': 1})
A.add_measurement(test_file2, treatment={'P_max':2, 'P': 2})
A.add_measurement(test_file3, treatment={'P_max': 3, 'P': 3})
A.add_measurement(test_file4, treatment={'P_max': 4, 'P': 4})
A.add_measurement(test_file5, treatment={'P_max': 5, 'P': 5})

A.difference(base={'P':0})
A.make_pdf(x='field', y='m', typ='differences')
verbous.RUNTIME()



# timing = []
# for i in range(1000):
#     A.measurements[0]._get_M()
#     timing.append(time.clock())
#
# print np.mean(timing)
