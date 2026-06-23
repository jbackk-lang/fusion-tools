import numpy as np

def timdr(signal, window=64):
    """
    TIMDR: redukcja informacji i wykrywanie defektów.
    """
    out = []
    for i in range(0, len(signal), window):
        chunk = signal[i:i+window]
        if len(chunk) < window:
            break
        out.append(np.mean(chunk))
    return np.array(out)
