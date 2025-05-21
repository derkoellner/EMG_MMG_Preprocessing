import numpy as np
from scipy.signal import butter, lfilter, iircomb, iirnotch

def butter_bandpass(lowcut, highcut, fs, order=5):
    return butter(order, [lowcut, highcut], fs=fs, btype='band')

def iir_comb(w0, fs, Q=30):
    return iircomb(w0, Q, fs=fs)

def iir_notch(w0, fs, Q=30):
    return iirnotch(w0, Q, fs=fs)

def filter_data(data, lowcut=5, highcut=400, w0=50, fs=1000, order=5, Q=30):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    if w0 != 0:
        b, a = iir_notch(w0, fs, Q)
        y = lfilter(b, a, y)
    return y

def standardize(data: np.ndarray) -> np.ndarray:
    dim = len(data.shape) 
    if dim == 1:
        avg = np.mean(data)
        std = np.std(data)

    elif dim == 2:
        avg = np.mean(data, axis=1, keepdims=True)
        std = np.std(data)

    elif dim == 3:
        avg = np.mean(data, axis=2, keepdims=True)
        std = np.std(data, axis=(1,2), keepdims=True)

    return (data - avg) / std