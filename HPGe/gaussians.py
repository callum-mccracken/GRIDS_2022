import numpy as np
import warnings

from read_spe import CHANNELS


def gauss(xvals, amp, mean, var):
    """Return a Gaussian with the given x values and parameters.

    xvals: numpy array of x values
    amp: number, amplitude of Gaussian
    mean: number, mean of Gaussian
    var: variance of Gaussian
    """
    #suppress warnings
    warnings.filterwarnings('ignore')

    return amp*np.exp(-(xvals-mean)**2/(2*var))


def comb_gauss(xvals, *params):
    """Return a sum of Gaussians.

    xvals: numpy array of x values
    params: list of parameters to pass, must have length being a multiple of 3
            (amplitude, mean, variance) for each Gaussian
    """
    assert len(params) % 3 == 0
    distr = 0
    for j in range(len(params) // 3):
        distr += gauss(xvals, *[params[j*3], params[j*3+1], params[j*3+2]])
    return distr
