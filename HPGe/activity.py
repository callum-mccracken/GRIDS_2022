import matplotlib.pyplot as plt
import numpy as np

from read_spe import data, Spectrum
from energy_calibration import channel_from_energy
from peak_data import known_peaks, Source

def activity(spec: Spectrum, peak_channel, tol, plot=True):
    start = peak_channel - tol
    stop = peak_channel + tol
    bkg_integral = np.sum(data.bkg.spectrum[start:stop]/data.bkg.live_time)
    smp_integral = np.sum(spec.spectrum[start:stop]/spec.live_time)
    peak_activity =  smp_integral - bkg_integral

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
    return peak_activity

class PeakActivities():
    def __init__(self, source: Source, spec: Spectrum,
                 tolerance=30, grams=None):
        self.source = source
        self.spec = spec

        peak_energies = source.peaks_kev
        peak_channels = [round(channel_from_energy(e)) for e in peak_energies]
        activities = np.array(
            [activity(spec, c, tolerance) for c in peak_channels])
        self.peak_activities = activities
        self.grams = grams
        self.activities_per_g = None if grams is None else activities/grams

Co60 = PeakActivities(known_peaks.Co60, data.Co60)
Ba133 = PeakActivities(known_peaks.Ba133, data.Ba133)
Na22 = PeakActivities(known_peaks.Na22, data.Na22)

if __name__ == "__main__":
    for sample in [Co60, Ba133, Na22]:
        print(f"Activities for source {sample.spec.name} "
            f"at energies {sample.source.peaks_kev} keV "
            f"are: {sample.peak_activities}")

