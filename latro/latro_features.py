import numpy as np

def latro_features(signal):
    """
    Ekstrahuje cechy Λ–τ–ρ dla sygnału.
    """
    lam, tau, rho = np.gradient(signal), np.std(signal), np.mean(signal)
    return {
        "lambda": np.mean(np.abs(lam)),
        "tau": tau,
        "rho": rho
    }
