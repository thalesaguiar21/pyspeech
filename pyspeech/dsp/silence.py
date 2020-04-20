import numpy as np

from . import processing as proc
from . import frame
from . import sphparams
from ..configs import confs


_IF = 35
_NEIGH_FRS = 20
_ITU = -15  #dB
ADJ_FRM = 25  # frames


def remove(signal, threshold):
    """ Removes silence from signal based on maximum aplitude

    Returns:
        The signal with amplitudes > threshold
    """
    or_frames = frame.striding(signal)
    norm_frames = frame.striding(proc.normalise(signal))
    voiced_indexes, __ = _detect_silence(norm_frames, threshold)
    voiced_frames = or_frames[voiced_indexes]
    voiced_amps = np.reshape(voiced_frames, voiced_frames.size)
    return proc.Signal(voiced_amps, signal.fs)


def discriminate(signal, normlen=10):
    """
    Args:
        signal: a signal to be labeled
        normlen (int, opt): number of frames to use when computing thresholds

    Returns:
        begins, ends : two lists with the indexes where the voice begins and
            ends, respectively
    """
    frames = frame.striding(signal)
    ibegins, iends = _get_words(frames, normlen)
    begins, ends = _adjust_words(frames, normlen, ibegins, iends)
    return begins, ends 


def _get_words(frames, normlen):
    energies = log_energy(frames)
    norm_egys = energies - max(energies)
    itr = get_itr(energies[:normlen])
    beginwords = _find_energy_peaks(energies, itr)
    rev_ends = _find_energy_peaks(energies.reverse(), itr)
    nframes = frames.shape[0]
    endwords = [nframes - rev for rev in rev_ends]
    return beginwords, endwords


def get_itr(energies):
    egyavg, egystd = np.mean(energies), np.std(energies)
    return max(_ITU, egyavg + 3*egystd)


def _find_energy_peaks(energies, itr):
    peaks = []
    for i, egy in enumerate(energies):
        if egy > itr:
            for negy in energies[i+_ADJ_FRM:i]:
                if negy < itr:
                    break
            else:
                peaks.append(i)
    return peaks


def _adjust_words(frames, normlen, begins, ends):
    zcrs = sphparams.zcr(frames)
    izct = get_izct(zcrs[:normlen])
    newbegins = _adjust(zcrs, begins, izct)
    newends = _adjust(zcrs.reverse(), ends, izct)
    return newends


def _adjust(words, zcrs, izct):
    adjusted_words = []
    for lblidx in words:
        low = np.inf
        highs = 0
        start = lblidx - _ADJ_FRM
        for j, zcr in enumerate(zcrs[start:lblidx]):
            if zcr > izct:
                highs += 1
                if low > start + j:
                    low = start + j

        if highs > 4:
            adjusted_words.append(low)
        else:
            adjusted_wods.append(lblidx)
    return adjusted_words


def get_izct(zcrs):
    zcavg, zcstd = np.mean(zcrs), np.std(zcrs)
    return max(_IF, zcavg + 3*zcstd)


def _detect_silence(frames, threshold):
    non_sil_indexes = []
    sil_indexes = []
    for i, frm_energy in enumerate(_db_energy(frames)):
        if frm_energy > threshold:
            non_sil_indexes.append(i)
        else:
            sil_indexes.append(i)
    return non_sil_indexes, sil_indexes


def _db_energy(signals):
    for signal in signals:
        sqr_sum = np.sum(signal ** 2)
        yield 10 * np.log(sqr_sum)
