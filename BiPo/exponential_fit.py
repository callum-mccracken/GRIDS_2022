"""
A module to make a fit of counts as a function of delay,
for the BiPo experiment.
"""

from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 22})

FIT_POINTS = [
    # (delay in nanoseconds, time in seconds, counts)
    # these are from a spreadsheet,
    # could read from a csv but no need, it's just a few points
    (560, 900, 80),
    (410, 900, 100),
    (290, 900, 164),
    (165, 900, 597),
    (210, 900, 308),
    (350, 900, 128),
]

# initial guesses for a, b, lam in a + be^(-t * lam)
GUESSES = (1, 4, 2e-3)  # based on the trendline from the spreadsheet


def fit_func(delay_time, constant_offset, y_scale, lambda_):
    """the function we want to fit"""
    return constant_offset+y_scale*np.exp(-delay_time*lambda_)


def main():
    """make a fit, calculate half-life, make a plot"""
    delays, times, counts = map(np.array, list(zip(*FIT_POINTS)))
    counts_per_sec = counts / times
    err_in_cps = np.sqrt(counts) / times
    fit_params, fit_covariances = curve_fit(
        fit_func, delays, counts_per_sec, p0=GUESSES, sigma=err_in_cps)
    # underscore on the lambda to avoid overwriting builtin lambda
    constant_offset, y_scale, lambda_ = fit_params

    half_life = np.log(2)/lambda_

    # plot data with error bars
    plt.figure(figsize=(8, 8))
    plt.scatter(delays, counts_per_sec)
    plt.errorbar(
        delays, counts_per_sec,
        # xerr=calc_act_uncerts,
        yerr=err_in_cps,
        fmt='o', ecolor='k', color='k')

    fit_line_delays = np.arange(min(delays), max(delays), 1)
    fit_line_cps = fit_func(fit_line_delays, *fit_params)
    fit_param_error = np.sqrt(np.diag(fit_covariances))
    const_err, scale_err, decay_err = fit_param_error

    print(f"The fit: {constant_offset:.2f}+{y_scale:.2f}*exp(-{lambda_:.2f}t)")
    half_life_low = np.log(2)/(lambda_ + decay_err)
    half_life_high = np.log(2)/(lambda_ - decay_err)
    print(f"Calculated half life {half_life:.2f} ns")
    print(f"±1σ half-life band: [{half_life_low}, {half_life_high}]")
    plt.xlabel("Delay [ns]")
    plt.ylabel("Counts per second")
    plt.plot(fit_line_delays, fit_line_cps, 'g')
    plt.tight_layout()
    plt.savefig("BiPo.png")


if __name__ == "__main__":
    main()
