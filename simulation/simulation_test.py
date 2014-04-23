__author__ = 'Mike'
from lmfit import Parameters
import paleointensity

params = Parameters()
params.add('amp', value=1)
params.add('mu', value=400)
params.add('sig', value=100.)
params.add('skew', value=-10.)
params.add('delta_mu', value=10)
params.add('delta_sig', value=-10)
params.add('delta_skew', value=0)

paleointensity.get_data(params)