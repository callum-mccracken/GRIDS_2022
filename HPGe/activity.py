"""A module for dealing with activity calculations."""
import matplotlib.pyplot as plt
import numpy as np
from inspect import cleandoc

from read_spe import data, Spectrum
from energy_calibration import channel_from_energy, energy_from_channel
from peak_data import known_peaks, Source
import peaks


def activity(spec: Spectrum, peak_channel, tol, plot=True):
    """Calculate activity of the source from spec, in the given peak."""
    start = peak_channel - tol
    stop = peak_channel + tol
    bkg_sum = np.sum(data.bkg.spectrum[start:stop])
    bkg_sum_norm = bkg_sum/data.bkg.live_time
    smp_sum = np.sum(spec.spectrum[start:stop])
    smp_sum_norm = smp_sum/spec.live_time
    peak_activity = smp_sum_norm - bkg_sum_norm
    uncertainty = np.sqrt(bkg_sum)  # number of counts

    if plot:
        plt.figure(figsize=(10, 10))
        plt.plot(data.bkg.spectrum/data.bkg.live_time, label=data.bkg.label)
        plt.plot(spec.spectrum/spec.live_time, label=spec.label)
        plt.ylim(0, 1.1*spec.spectrum[peak_channel]/spec.live_time)
        plt.xlim(start, stop)
        plt.legend(fontsize=30)
        output_filename = spec.filename.replace(
            ".Spe", f"_peak_{peak_channel}.png")
        output_filename = output_filename.replace(
            "data", "images")
        plt.savefig(output_filename)
        plt.cla()
        plt.clf()
    return peak_activity, uncertainty


class PeakActivities():
    """Class for storing activities at peaks for a given source/spectrum."""

    def __init__(self, source: Source, spec: Spectrum,
                 tolerance=30, grams=None):
        """Create object using peak energies from source."""
        self.source = source
        self.spec = spec
        peak_energies = source.peaks_kev
        peak_channels = [round(channel_from_energy(e)) for e in peak_energies]
        activities_uncertainties = np.array(
            [activity(spec, c, tolerance) for c in peak_channels])
        activities, uncertainties = list(zip(*activities_uncertainties))
        self.uncertainties = uncertainties
        self.calc_peak_activities = activities
        self.real_peak_activities = None  # to be set later
        self.grams = grams
        self.activities_per_g = None if grams is None else activities/grams


Co60 = PeakActivities(known_peaks.Co60, data.Co60)
Ba133 = PeakActivities(known_peaks.Ba133, data.Ba133)
Na22 = PeakActivities(known_peaks.Na22, data.Na22)


def current_activity(A0, time, half_life):
    '''
    Returns current activity in Bq
    inputs:
        A0 [Bq]
        time [days]
        half_life [days]
    '''
    return A0*np.exp(-(time*np.log(2))/half_life)


na22_current_act = current_activity(37e3, 762, 2.6018*365)
co60_current_act = current_activity(3.7e5, 16390, 1925.28)
ba133_current_act = current_activity(3.81e5, 6925, 10.551*365)

real_na22_acts = list(
    na22_current_act * np.array(known_peaks.Na22.intensities))
real_ba133_acts = list(
    ba133_current_act * np.array(known_peaks.Ba133.intensities))
real_co60_acts = list(
    co60_current_act * np.array(known_peaks.Co60.intensities))

calc_na22_acts = list(Na22.calc_peak_activities)
calc_ba133_acts = list(Ba133.calc_peak_activities)
calc_co60_acts = list(Co60.calc_peak_activities)

real_activities = real_co60_acts + real_ba133_acts + real_na22_acts
calc_activities = calc_co60_acts + calc_ba133_acts + calc_na22_acts

# need real = line(calculated)
act_line = np.polyfit(calc_activities, real_activities, deg=1)
activity_x_values = np.arange(min(calc_activities), max(calc_activities), 1)
fit_activities = np.polyval(act_line, activity_x_values)

plt.figure(figsize=(15, 15))
plt.xlabel("calculated activity")
plt.ylabel("real activity")
plt.scatter(calc_activities, real_activities)
plt.plot(activity_x_values, fit_activities)
plt.savefig("images/activity_calibration.png")
plt.cla()
plt.clf()

Na22.real_peak_activities = np.polyval(act_line, Na22.calc_peak_activities)
Ba133.real_peak_activities = np.polyval(act_line, Ba133.calc_peak_activities)
Co60.real_peak_activities = np.polyval(act_line, Co60.calc_peak_activities)


if __name__ == "__main__":
    x_peak_channels, x_peak_stdevs = peaks.get_peaks(
        data.x, n_peaks=1, background_width=100, plot=True)
    x_peak_channel = x_peak_channels[0]
    x_peak_stdev = x_peak_stdevs[0]
    x_peak_energies = [energy_from_channel(x_peak_channel)]

    x_activities = PeakActivities(Source(x_peak_energies), data.x)
    x_activities.real_peak_activities = np.polyval(
        act_line, x_activities.calc_peak_activities)

    samples = [Co60, Ba133, Na22, x_activities]

    peak_stdevs = [
        peaks.co_peak_stdevs,
        peaks.ba_peak_stdevs,
        peaks.na_peak_stdevs,
        x_peak_stdevs,
        ]

    for sample, stdevs in zip(samples, peak_stdevs):
        print(cleandoc(f"""
            For source {sample.spec.name}:
                Peak energies [keV] = {sample.source.peaks_kev}
                Energy uncertainties [keV] = {[round(s, 2) for s in stdevs]}
                Peak activities [Bq] = {
                    [round(s, 2) for s in sample.real_peak_activities]}
                Activity uncertainties [sqrt(n)]= {
                    [round(s, 2) for s in sample.uncertainties]}
            """))
