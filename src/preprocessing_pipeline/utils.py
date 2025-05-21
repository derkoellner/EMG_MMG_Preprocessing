import numpy as np

def _check_signal_dim(data: np.ndarray):
    if data.ndim == 1:
        return data.reshape(1,-1)
    elif data.ndim == 2:
        return data
    else:
        raise ValueError('Signal is either empty or has more than 2 Dimensions!')

