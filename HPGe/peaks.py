"""Module for detecting / fitting peaks."""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

from read_spe import data, Spectrum, CHANNELS
from gaussians import comb_gauss
from peak_data import known_peaks


def integral(spectrum: Spectrum, range_tuple, step=1):
    """
    Return the "integral" (sum * step size) of a spectrum.

    Calculated over some range given by a tuple (start, stop).

    spectrum: Spectrum object, to be integrated
    range_tuple: tuple of numbers, (start, stop)
    step: number, step size, default 1 only needs to be changed
          if we're no longer integrating over channels
    """
    start, stop = range_tuple
    return np.sum(spectrum.spectrum[start:stop]/spectrum.live_time) * step


def activity(sample_spectrum: Spectrum, peak_channel_range, step=1):
    """
    Return the activity of a sample, using a peak.

    activity = sample peak integral - background peak integral

    sample_spectrum: Spectrum object, for which to calculate activity
    peak_channel_range: (start, stop) of the peak
    step: number, step size, default 1 only needs to be changed
          if we're no longer integrating over channels
    """
    bkg_integral = integral(data.bkg, peak_channel_range, step=step)
    smp_integral = integral(sample_spectrum, peak_channel_range, step=step)
    return smp_integral - bkg_integral


def get_peaks(spec: Spectrum, n_peaks=1, peak_prominence=100, peak_width=5,
              background_width=70, plot=False):
    """
    Get the largest n_peaks peaks in a given spectrum.

    spec: Spectrum object, for which to find peaks
    n_peaks: int, we'll find some number of best peaks
    peak_prominence: peaks must have at least this prominence
    peak_width: peaks must have at least this width
    background_width: take this width on either side of each peak
    """
    # find peak points and properties (like width)
    peak_chs, properties = find_peaks(
        spec.spectrum, prominence=peak_prominence, width=peak_width)
    if len(peak_chs) < n_peaks:
        print(peak_chs)
        print(spec.spectrum[peak_chs])
        raise ValueError(
            f"Less peaks found than are required {len(peak_chs)} < {n_peaks}. "
            "Try changing peak parameters like prominence and width.")

    # find the n_peaks highest peaks
    proms = properties["prominences"]
    best_indices = np.array((proms >= sorted(proms)[-n_peaks]), dtype=bool)
    peak_chs = peak_chs[best_indices]
    properties = {k: properties[k][best_indices] for k in properties}
    # print("peaks before fitting: ", list(zip(peaks, spec.spectrum[peaks])))

    # now select background regions around peaks
    widths = properties["widths"]
    background_regions = []
    for peak, width in zip(peak_chs, widths):
        left = peak - 2*width
        right = peak + 2*width
        background_regions.append((left - background_width, left))
        background_regions.append((right, right + background_width))
    mask_bkg = np.ones_like(CHANNELS, dtype=bool)
    for start, stop in background_regions:
        mask_bkg = mask_bkg ^ ((CHANNELS > start) * (CHANNELS < stop))

    # and fit a sum of Gaussians to the peaks
    initial_guesses = []
    for peak in peak_chs:
        initial_guesses += [1000, peak, 10]
    coeff = np.polyfit(CHANNELS[mask_bkg], spec.spectrum[mask_bkg], 2)
    bkgfit = np.polyval(coeff, CHANNELS)
    coeff_gauss, *_ = curve_fit(
        comb_gauss, CHANNELS, spec.spectrum-bkgfit, p0=initial_guesses)
    fit_hist = comb_gauss(CHANNELS, *coeff_gauss)

    fit_peaks = coeff_gauss[[i*3+1 for i in range(len((peak_chs)))]]

    # now plot if needed
    if plot:
        plt.figure(figsize=(50, 10))
        plt.plot(CHANNELS, spec.spectrum, label=spec.label)
        plt.plot(CHANNELS, bkgfit, label='background fit')
        plt.plot(CHANNELS, fit_hist, label='Gaussian peak fit')
        for peak in fit_peaks:
            plt.axvline(peak, c='r')
        for start, stop in background_regions:
            plt.axvspan(start, stop, alpha=0.1, color='m')
        plt.legend(fontsize=30)
        plt.xlim(min(peak_chs) - 1.5*background_width,
                 max(peak_chs) + 1.5*background_width)
        plt.savefig(f"images/peaks_{spec.name}.png")
        plt.cla()
        plt.clf()
    return list(fit_peaks)


co_peak_channels = get_peaks(
    data.Co60, n_peaks=2, background_width=100, plot=True)
ba_peak_channels = get_peaks(
    data.Ba133, n_peaks=5, background_width=70, plot=True)
# ignore annihilation peak at 511keV, find 2 peaks and take 2nd one
na_peak_channels = [get_peaks(
    data.Na22, n_peaks=2, background_width=400, plot=True)[1]]

# see which peaks correspond to which real peaks
co_peak_energies = known_peaks.Co60.peaks_kev
ba_peak_energies = known_peaks.Ba133.peaks_kev
na_peak_energies = known_peaks.Na22.peaks_kev

peak_channels = co_peak_channels + ba_peak_channels + na_peak_channels
peak_energies = co_peak_energies + ba_peak_energies + na_peak_energies

# to be used in energy_calibration.py
peaks = [(chan, energy) for chan, energy in zip(peak_channels, peak_energies)]
