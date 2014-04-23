__author__ = 'Mike'
from lmfit import Parameters
import paleointensity

params = Parameters()
params.add('amp', value=1)
params.add('center', value=528.9)
params.add('sig', value=50.)
params.add('skew', value=-10.)

paleointensity.get_data(params)