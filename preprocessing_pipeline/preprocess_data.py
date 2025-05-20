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
