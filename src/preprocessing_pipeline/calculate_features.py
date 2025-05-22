import numpy as np
from scipy.signal import stft

from .utils import _check_signal_dim

def prepare_spectrogram(data: np.ndarray,
                        window_length: int,
                        window: str,
                        hop: int,
                        fs: int,
                        f_max: int,
                        log: bool = True):
    spectrogram_data = None

    for idx, trial in enumerate(data):
        spec, f, t = calculate_spectrogram(trial, window_length=window_length, fs=fs, f_max=f_max, hop=hop, window=window, log=log)
        if spectrogram_data is None:
            n_channels, n_freq_bins, n_t_bins = spec.shape
            trials = data.shape[0]
            spectrogram_data = np.empty(shape=(trials, n_channels, n_freq_bins, n_t_bins))
        
        spectrogram_data[idx,:,:,:] = spec
        print(f'Finished Trial {idx}')

    return spectrogram_data

def calculate_spectrogram(data: np.ndarray,             # E/MMG Data
                          window_length: int = 200,     # Sliding window length
                          window: str = 'hann',         # Window type, possible are 'hann', 'hamming', 'gaussian'
                          hop: int = 10,                # Increment of the sliding window
                          fs: int = 1000,               # Sampling Frequency of the data
                          f_max: int = 200,             # Maximum Frequency to be returned
                          log = True) -> np.ndarray:    # If the spectrogram values should be returned as a logarithmic scale

    data = _check_signal_dim(data)
    noverlap = window_length-hop
    spectrogram_list = []

    for channel in data:
        f, t, Zxx = stft(channel, fs=fs, nperseg=window_length, noverlap=noverlap, window=window)

        freq_mask = f <= f_max
        f = f[freq_mask]
        Zxx = np.abs(Zxx[freq_mask,:])**2

        if log:
            Zxx = np.log1p(Zxx)

        spectrogram_list.append(Zxx)

    spectrogram = np.stack(spectrogram_list, axis=0)

    return spectrogram, f, t