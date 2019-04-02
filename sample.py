from processing import process_voice_dataset, fft
from features import mfcc, log_energy, energy_delta
from filters import compute_filter_banks
import pdb


windowed_signals = process_voice_dataset(
    'C:\\DATASETS\\english_small\\train\\voice',
    0.97,
    25,
    10
)

proc_fb = 1
total_fb = len(windowed_signals)
print('')

print('Computing log energy')
energies = log_energy(windowed_signals[0])
e_delta = energy_delta(energies)
e_delta2 = energy_delta(e_delta)
pdb.set_trace()

for frames in windowed_signals:
    print('AUDIO ', proc_fb, '/', total_fb, '...', end='\r', sep='')
    pow_frames = fft(frames, 512)
    fbanks = compute_filter_banks(pow_frames, 40, 16000, 512)
    mfcc(fbanks, 12)
    proc_fb += 1
