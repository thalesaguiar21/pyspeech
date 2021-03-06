import math
import unittest

import numpy as np

from .context import pyspeech
import pyspeech.dsp.processing as sp


class TestsMinNFFT(unittest.TestCase):

    def test_inside(self):
        nfft = sp.find_best_nfft(16000, 0.025)
        self.assertEqual(512, nfft)

    def test_negative_freq(self):
        with self.assertRaises(ValueError):
            sp.find_best_nfft(-30, 0.025)

    def test_negative_winlen(self):
        with self.assertRaises(ValueError):
            sp.find_best_nfft(1600, -1)

    def test_nfft_power_of_2(self):
        nfft = sp.find_best_nfft(13093, 0.025)
        self.assertEqual(is_power_of_2(nfft), True)


def is_power_of_2(x):
    return math.ceil(math.log2(x)) == math.floor(math.log2(x))


class TestsNormalise(unittest.TestCase):

    def test_inside(self):
        signal = sp.Signal(np.arange(2*200), 200)
        normalised_signal = sp.normalise(signal)
        expected = np.arange(2*200) / 399
        self.assertNumpyArrayEqual(expected, normalised_signal.amps)

    def test_negative_amps(self):
        signal = sp.Signal(np.arange(-300, 100), 200)
        normalised_signal = sp.normalise(signal)
        expected = np.arange(-300, 100) / 300
        self.assertNumpyArrayEqual(expected, normalised_signal.amps)

    def test_zero_as_max(self):
        signal = sp.Signal(np.arange(2*200) * 0.0, 200)
        normalised_signal = sp.normalise(signal)
        expected = np.arange(2*200) * 0.0
        self.assertNumpyArrayEqual(expected, normalised_signal.amps)

    def assertNumpyArrayEqual(self, left, right):
        left_list = left.tolist()
        right_list = right.tolist()
        self.assertListEqual(left_list, right_list)

