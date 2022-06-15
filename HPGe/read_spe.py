import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

N_CHANNELS = 8191
START_LINE = 13

BACKGROUND_FILE = "run3_background.Spe"

def read(spe_filename):
    """given a .Spe file, return the data as a numpy array"""
    with open(spe_filename, "r", encoding="utf-8") as spe_file:
        spe_lines = spe_file.readlines()
    data_lines = spe_lines[START_LINE:START_LINE+N_CHANNELS]
    data_nums = [int(d.strip().replace("\n", "")) for d in data_lines]
    return np.array(data_nums)


def plot(spe_filename: str, with_bkg=False, save=True, plot_peaks=True):
    """given a spe filename, make a plot -- either save or return the data"""
    data = read(spe_filename)
    if with_bkg:
        plot_data = data
        output_filename = spe_filename.replace(".Spe", ".png")
        xlabel = spe_filename+" channel number"
    else:
        plot_data = data - read(BACKGROUND_FILE)
        output_filename = spe_filename.replace(".Spe", "_nobkg.png")
        xlabel = spe_filename+" (bkg removed) channel number"
    plt.ylabel("counts")
    plt.plot(plot_data)
    plt.xlabel(xlabel)

    if plot_peaks:
        peaks, properties = find_peaks(plot_data, prominence=100, width=1)
        print(peaks)
        plt.plot(peaks, plot_data[peaks], "x")
        plt.vlines(x=peaks, ymin=plot_data[peaks] - properties["prominences"],
                   ymax = plot_data[peaks], color = "C1")
        plt.hlines(y=properties["width_heights"], xmin=properties["left_ips"],
                   xmax=properties["right_ips"], color = "C1")



    if save:
        plt.savefig(output_filename)
        plt.cla(); plt.clf()
    else:
        return plot_data



if __name__ == "__main__":
    # plot background
    plot("run3_background.Spe", with_bkg=True)
    # this one should be all zero
    plot("run3_background.Spe")
    # plot other isotopes
    plot("run2_co60.Spe")
    plot("run4_ba133.Spe")
    plot("run5_na22.Spe")
    plot("run6_mistery_source.Spe")



