import numpy as np

def model_j(signal, threshold=2.0):
    """
    Model J: detekcja punktów skrętu sygnału.
    """
    grad = np.gradient(signal)
    z = (grad - np.mean(grad)) / np.std(grad)
    return np.where(np.abs(z) > threshold)[0]
