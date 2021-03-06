import unittest
import numpy as np

from .context import pyspeech
import pyspeech.dsp.processing as sp
import pyspeech.features.mfcc as mfcc
from pyspeech import conf


class TestsMFCC(unittest.TestCase):

    def setUp(self):
        self.emph = 0.97
        self.signnal = sp.Signal([], 0)
        conf.append_energy = True
        conf.framing['size'] = 25
        conf.framing['stride'] = 10

    def test_signal_200l_20hz(self):
        self.make_signal(32000, 8000)
        mfccs = self.extract()

    def test_has_energy(self):
        self.make_signal(32000, 8000)
        mfccs = self.extract()
        self.assertEqual(mfccs.shape[1], 13)

    def test_no_energy_append(self):
        self.make_signal(32000, 8000)
        conf.append_energy = False
        mfccs = self.extract()
        self.assertEqual(mfccs.shape[1], 12)

    def test_no_zero(self):
        self.make_signal(32000, 8000)
        mfccs = self.extract()
        nzeros = np.count_nonzero(mfccs) - mfccs.size
        self.assertEqual(0, nzeros)

    def make_signal(self, slen, samplerate):
        amps = np.arange(slen)
        self.signal = sp.Signal(amps, samplerate)

    def extract(self):
        return mfcc.extract(self.signal, self.emph, 40, (300, 3700))

