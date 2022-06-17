from dataclasses import dataclass


@dataclass
class Source():
    peaks_kev: list  # energies in keV
    intensities: list


@dataclass
class KnownPeaks:
    Co60 = Source(
        [1173.288, 1332.492],
        [99.85, 99.9826])
    Ba133 = Source(
        [80.9979, 276.3989, 302.8508, 356.0129, 383.8485],
        [32.9, 7.16, 18.34, 62.05, 8.94])
    Na22 = Source([1274.5], [99.94])


known_peaks = KnownPeaks()
