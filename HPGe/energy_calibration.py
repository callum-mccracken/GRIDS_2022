"""Module for getting a relationship between channels and energies."""
import matplotlib.pyplot as plt
import numpy as np

from read_spe import CHANNELS
from peaks import peaks

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
    plt.figure(figsize=(15, 15))
    plt.scatter(*list(zip(*peaks)))
    plt.savefig("images/peaks.png")
    # calculate channel from energy for an example energy
    print(channel_from_energy(1274.5))