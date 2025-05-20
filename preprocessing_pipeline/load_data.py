import mne
import numpy as np
from scipy.io import loadmat, matlab
from pyctf.dsopen import dsopen

def load_mne_raw(filepath: str, picks: str = None, return_fs: bool = False):
    raw = mne.io.read_raw_fif(filepath, preload=True)

    if picks is None:
        return raw
    
    data = raw.get_data(picks=picks)

    if return_fs:
        fs = raw.info['sfreq']
        return data, fs
    else:
        return data

def load_mat_file(filename):
    """
    This function should be called instead of direct scipy.io.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    """

    def _check_vars(d):
        """
        Checks if entries in dictionary are mat-objects. If yes
        todict is called to change them to nested dictionaries
        """
        for key in d:
            if isinstance(d[key], matlab.mio5_params.mat_struct):
                d[key] = _todict(d[key])
            elif isinstance(d[key], np.ndarray):
                d[key] = _toarray(d[key])
        return d

    def _todict(matobj):
        """
        A recursive function which constructs from matobjects nested dictionaries
        """
        d = {}
        for strg in matobj._fieldnames:
            elem = matobj.__dict__[strg]
            if isinstance(elem, matlab.mio5_params.mat_struct):
                d[strg] = _todict(elem)
            elif isinstance(elem, np.ndarray):
                d[strg] = _toarray(elem)
            else:
                d[strg] = elem
        return d
    
    def _toarray(ndarray):
        """
        A recursive function which constructs ndarray from cellarrays
        (which are loaded as numpy ndarrays), recursing into the elements
        if they contain matobjects.
        """
        if ndarray.dtype != 'float64':
            elem_list = []
            for sub_elem in ndarray:
                if isinstance(sub_elem, matlab.mio5_params.mat_struct):
                    elem_list.append(_todict(sub_elem))
                elif isinstance(sub_elem, np.ndarray):
                    elem_list.append(_toarray(sub_elem))
                else:
                    elem_list.append(sub_elem)
            return np.array(elem_list)
        else:
            return ndarray

    data = loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_vars(data)['SQUID']

def load_ctf_file(filepath: str, channel_names: list = ['EEG057', 'EEG058', 'UADC002'], return_fs: bool = False) -> np.ndarray:
    EMG = dsopen(filepath)
    n_samples = EMG.getNumberOfSamples()

    data = np.zeros((3, n_samples))

    for idx, channel_name in enumerate(channel_names):

        channel = EMG.getDsRawData(tr=0, ch=EMG.getChannelIndex(channel_name))

        data[idx] = channel - np.mean(channel)

    if return_fs:
        fs = EMG.getSampleRate()
        return data, fs
    else:
        return data