import numpy as np

def latro(signal):
    """
    Λ–τ–ρ: analiza struktury sygnału.
    Zwraca: (lambda, tau, rho)
    """
    grad = np.gradient(signal)
    lam = np.mean(np.abs(grad))
    tau = np.std(grad)
    rho = np.mean(signal)
    return lam, tau, rho
