"""Module for storing plotting functions."""
import matplotlib.pyplot as plt

from read_spe import Spectrum, CHANNELS, data


def make_normalized_plot(spectra, labels):
    """Make a normalized plot of all given spectra, using labels for legend."""
    for spec, lab in zip(spectra, labels):
        plt.plot(spec/max(spec), label=lab)
    plt.legend()
    plt.savefig("images/all_spectra_normalized.pdf")
    plt.cla()
    plt.clf()


def plot_spectrum(spec: Spectrum, save=True):
    """Given a spe filename, make a plot -- either save or return the data."""
    plot_data = spec.spectrum
    output_filename = spec.filename.replace(".Spe", ".pdf")
    output_filename = output_filename.replace("data", "images")
    xlabel = spec.filename+" channel number"
    plt.ylabel("counts")
    plt.plot(CHANNELS, plot_data)
    plt.xlabel(xlabel)

    if save:
        plt.savefig(output_filename)
        plt.cla()
        plt.clf()
    else:
        return plot_data


if __name__ == "__main__":
    specs = [
        data.Co60.spectrum,
        data.Ba133.spectrum,
        data.Na22.spectrum,
        data.x.spectrum,
        data.bkg.spectrum]
    labs = [
        data.Co60.label,
        data.Ba133.label,
        data.Na22.label,
        data.x.label,
        data.bkg.label]
    make_normalized_plot(specs, labs)

    plot_spectrum(data.Co60)
    plot_spectrum(data.Ba133)
    plot_spectrum(data.Na22)
    plot_spectrum(data.x)
    plot_spectrum(data.bkg)
