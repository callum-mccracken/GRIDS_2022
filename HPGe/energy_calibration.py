"""Module for getting a relationship between channels and energies."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from read_spe import data, CHANNELS
from peaks import peaks, peak_stdevs

plt.rcParams.update({'font.size': 22})

line = np.polyfit(*list(zip(*peaks)), deg=1)
energies = np.polyval(line, CHANNELS)


def energy_from_channel(channel):
    """Given a channel number, return the fit energy."""
    return line[0]*channel + line[1]


def channel_from_energy(energy):
    """
    Given an energy, return the corresponding channel number.

    (result may not be an integer!)
    """
    return (energy - line[1]) / line[0]


if __name__ == "__main__":
    # make a scatterplot

    peak_channels, peak_energies = list(zip(*peaks))

    plt.figure(figsize=(15, 15))
    plt.xlabel("Measured Channel [Mean of Gaussian Fit]")
    plt.ylabel("Known Energy [keV]")

    y_error = np.zeros_like(peak_channels)
    x_error = peak_stdevs
    print(x_error)

    plt.errorbar(
        peak_channels, peak_energies,
        xerr=x_error, yerr=y_error,
        fmt='o', ecolor='k', color='k')

    co_patch = mpatches.Patch(color='g', label=data.Co60.label)
    ba_patch = mpatches.Patch(color='b', label=data.Ba133.label)
    na_patch = mpatches.Patch(color='r', label=data.Na22.label)
    colors = ['g']*2 + ['b']*5 + ['r']*1
    plt.plot(CHANNELS, energies)
    plt.scatter(peak_channels, peak_energies, s=10,
                c=colors, marker="o", zorder=100, linewidths=5)

    plt.legend(handles=[co_patch, ba_patch, na_patch])

    plt.savefig("images/energy_calibration.pdf")
    plt.cla()
    plt.clf()

    # calculate channel from energy for an example energy
    print(channel_from_energy(1274.5))
