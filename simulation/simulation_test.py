__author__ = 'Mike'
from lmfit import Parameters
import paleointensity
import numpy as np
from fit import fitting, distributions
params = Parameters()
params.add('amp', value=1, min = 0.01, max = 100)
params.add('mu', value=520, min = 450, max = 580)
params.add('sig', value=15., min = 0, max=100)
params.add('skew', value=-1., min = -5, max=-2)
# params.add('delta_mu', value=10.)
# params.add('delta_sig', value=-0)
# params.add('delta_skew', value=0)

th_diff_data = np.array([[300.0, 0.00429753818747],
                         [450.0, 0.0130449494852],
                         [490.0, 0.0564667343796],
                         [500.0, 0.169588303259],
                         [510.0, 0.296940611517],
                         [515.0, 0.387253514572],
                         [520.0, 0.670335045597],
                         [525.0, 0.976217109089],
                         [530.0, 1.0],
                         [535.0, 0.790684044136],
                         [540.0, 0.446419409974],
                         [545.0, 0.216975215207]])
pt_diff_data = np.array([[300.0, 0.00262476957746],
                         [450.0, 0.00506146401176],
                         [490.0, 0.0140554195228],
                         [500.0, 0.0734268867254],
                         [510.0, 0.177056553028],
                         [515.0, 0.334763062977],
                         [520.0, 0.632050424137],
                         [525.0, 0.830605739006],
                         [530.0, 1.0],
                         [535.0, 0.834441758882],
                         [540.0, 0.44375000485],
                         [545.0, 0.227736623091]])
th_data = np.array([[20, 1.0],
                    [300, 0.961188090954],
                    [450, 0.94141148082],
                    [490, 0.882606589251],
                    [500, 0.851898298387],
                    [510, 0.775071496988],
                    [515, 0.71068188439],
                    [520, 0.652293741629],
                    [525, 0.498153839736],
                    [530, 0.342786556058],
                    [535, 0.181106348263],
                    [540, 0.092102163317],
                    [545, 0.0395701941854],
                    [550, 0.0233107156236]])
pt_data = np.array([[20, 0.0],
                    [300, 0.0384587117221],
                    [450, 0.0444864219073],
                    [490, 0.0763638068851],
                    [500, 0.0721865421498],
                    [510, 0.134247062181],
                    [515, 0.176868322739],
                    [520, 0.266195839407],
                    [525, 0.425994614835],
                    [530, 0.593583845253],
                    [535, 0.820150338148],
                    [540, 0.922483840287],
                    [545, 0.995056942279],
                    [550, 1.01224753369]])

fit, fit_pa = fitting.normal_skewed(th_diff_data[:,0], th_diff_data[:,1], parameters=params, dfunc='pdf', check=True)

# paleointensity.get_data(parameters=params, data_th=th_diff_data, data_ptrm=pt_diff_data)