import structure.experiments as exp
import verbous
import matplotlib.pyplot as plt
from pprint import pprint
import time
import numpy as np

# file ='/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/NLCRY-LF4C_P0-140220.TT'
#
# exp = exp.TreatmentPint(parameters={})
# exp.add_measurement(file)

def test_P_demag():
    test_file0 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P00.AF'
    test_file1 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P11.AF'
    test_file2 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P22.AF'
    test_file3 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P33.AF'
    test_file4 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P44.AF'
    test_file5 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P55.AF'
    test_file6 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P66.AF'
    IRMtest_file0 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P00.IRM'
    IRMtest_file1 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P11.IRM'
    IRMtest_file2 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P22.IRM'
    IRMtest_file3 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P33.IRM'
    IRMtest_file4 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P44.IRM'
    IRMtest_file5 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P55.IRM'
    IRMtest_file6 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P66.IRM'
    test_file10 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P10.AF'
    test_file20 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P20.AF'
    test_file30 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P30.AF'
    test_file40 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P40.AF'
    test_file50 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P50.AF'
    test_file60 = '/Users/Mike/Dropbox/__PHD/__Projects/001 Influence of Pressure on Paleointensities/04 data/LF4C/pressure_demag/LF4c-6c_pdemag_P60.AF'

    A = exp.TreatmentAF(parameters={}, sample='LF4C-6c')
    A.add_measurement(sample='LF4C-6c', file=test_file0, treatment={'P_max': 0, 'P': 0})
    A.add_measurement(test_file1, treatment={'P_max': 1, 'P': 1})
    A.add_measurement(test_file2, treatment={'P_max': 2, 'P': 2})
    A.add_measurement(test_file3, treatment={'P_max': 3, 'P': 3})
    A.add_measurement(test_file4, treatment={'P_max': 4, 'P': 4})
    A.add_measurement(test_file5, treatment={'P_max': 5, 'P': 5})
    A.add_measurement(test_file6, treatment={'P_max': 6, 'P': 6})
    # A.add_measurement(test_file10, treatment={'P_max': 1, 'P': 0})
    # A.add_measurement(test_file20, treatment={'P_max': 2, 'P': 0})
    # A.add_measurement(test_file30, treatment={'P_max': 3, 'P': 0})
    # A.add_measurement(test_file40, treatment={'P_max': 4, 'P': 0})
    # A.add_measurement(test_file50, treatment={'P_max': 5, 'P': 0})
    # A.add_measurement(test_file60, treatment={'P_max': 6, 'P': 0})

    A.contour_treatment2(mode='differences')
    A.data_vs_treatment()
    A.make_pdf(x='field', y='m', differences={'P': 0})
    # A.contour_treatment(mode='differences')
    plt.show()


test_P_demag()
verbous.RUNTIME()



# timing = []
# for i in range(1000):
#     A.measurements[0]._get_M()
#     timing.append(time.clock())
#
# print np.mean(timing)
