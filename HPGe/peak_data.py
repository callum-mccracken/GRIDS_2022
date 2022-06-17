"""Module for storing known data about peaks."""
from dataclasses import dataclass


@dataclass
class Source():
    """Class for storing peak energies and intensities (as lists)."""

    peaks_kev: list  # energies in keV
    intensities: list = None


@dataclass
class KnownPeaks:
    """Class for storing data we know (from the internet) about peaks."""

    Co60 = Source(
        [1173.288, 1332.492],
        [.9985, .999826])
    Ba133 = Source(
        [80.9979, 276.3989, 302.8508, 356.0129, 383.8485],
        [.329, .0716, .1834, .6205, .0894])
    Na22 = Source([1274.5], [.9994])


known_peaks = KnownPeaks()
