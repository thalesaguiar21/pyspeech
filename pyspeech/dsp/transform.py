import numpy as np


def make_power_spectrum(frames, nfft):
    mag_spectrum = np.absolute(np.fft.rfft(frames, nfft))
    return 1.0/nfft * mag_spectrum**2.0
