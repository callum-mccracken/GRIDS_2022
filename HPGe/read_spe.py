"""module for reading data from .Spe files"""

from dataclasses import dataclass
import numpy as np

N_CHANNELS = 8191
START_LINE = 13

CHANNELS = np.arange(0, N_CHANNELS, 1)
CO60_FILE = 'data/frun3_co60_live180s.Spe'
BA133_FILE = 'data/frun1_ba133_live180s.Spe'
NA22_FILE = 'data/frun2_na22_live180s.Spe'
X_FILE = 'data/frun4_source_live5400s.Spe'
BKG_FILE = 'data/frun5_bkg_live5400s.Spe'


def read(spe_filename):
    """given a .Spe file, return the data as a numpy array"""
    with open(spe_filename, "r", encoding="utf-8") as spe_file:
        spe_lines = spe_file.readlines()
    data_lines = spe_lines[START_LINE:START_LINE+N_CHANNELS]
    data_nums = [int(d.strip().replace("\n", "")) for d in data_lines]
    return np.array(data_nums)


def read_time(spe_filename):
    """get live_time and real_time from a .Spe file"""
    with open(spe_filename, "r", encoding="utf-8") as spe_file:
        time_line = spe_file.readlines()[9]  # example: 245 245
        time_line = time_line.strip().replace("\n", "")
        live, real = map(int, time_line.split())
    return live, real


def live_time(spe_filename):
    """get live_time from a .Spe file"""
    return read_time(spe_filename)[0]


def real_time(spe_filename):
    """get live_time from a .Spe file"""
    return read_time(spe_filename)[1]


class Spectrum():
    """Class for keeping track of spectrum names & data."""
    def __init__(self, name: str, label: str, filename: str) -> None:
        self.name = name
        self.label = label
        self.filename = filename
        self.spectrum = read(self.filename)
        self.live_time = live_time(self.filename)


@dataclass
class SpeData():
    Co60 = Spectrum("Co60", r'$^{60}Co$', CO60_FILE)
    Ba133 = Spectrum("Ba133", r'$^{133}Ba$', BA133_FILE)
    Na22 = Spectrum("Na22", r'$^{22}Na$', NA22_FILE)
    bkg = Spectrum("bkg", 'background', BKG_FILE)
    x = Spectrum("x", 'X', X_FILE)

data = SpeData()
