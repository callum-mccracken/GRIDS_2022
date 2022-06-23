"""
A module to make a fit of counts as a function of delay,
for the BiPo experiment.
"""

from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

FIT_POINTS = [
    # (delay in nanoseconds, counts per sec)
    # these are from a spreadsheet,
    # could read from a csv but no need, it's just a few points
    (188, 2.333333333),
    (261, 1.633333333),
    (319, 1.257142857),
    (314, 1.419047619),
    (309, 1.352380952),
    (573, 1.008333333),
    (705, 0.9833333333),
    (441, 1.108333333),
    (393, 1.1),
    (261, 2.133333333),
    (324, 1.666666667),
    (324, 1.6),
]

# initial guesses for a, b, lam in a + be^(-t * lam)
GUESSES = (1, 4, 2e-3)  # based on the trendline from the spreadsheet


def fit_func(delay_time, constant_offset, y_scale, lambda_):
    """the function we want to fit"""
    return constant_offset+y_scale*np.exp(-delay_time*lambda_)


def main():
    """make a fit, calculate half-life, make a plot"""
    delays, counts = map(np.array, list(zip(*FIT_POINTS)))
    fit_params, *_ = curve_fit(fit_func, delays, counts, p0=GUESSES)
    _, _, lam = fit_params

    half_life = np.log(2)/lam

    print(f"{half_life = } ns")

    fit_line_delays = np.arange(min(delays), max(delays), 1)
    fit_line_counts = fit_func(fit_line_delays, *fit_params)

    # plot
    plt.scatter(delays, counts)
    plt.plot(fit_line_delays, fit_line_counts)
    plt.savefig("BiPo.png")


if __name__ == "__main__":
    main()
