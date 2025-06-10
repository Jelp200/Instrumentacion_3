import numpy as np

def build_accumulator_matrix(W, R):
    if R > W:
        raise ValueError("R no debe ser mayor que W.")
    H = np.zeros((R, W))
    indices = np.linspace(0, W, R + 1, dtype=int)
    for i in range(R):
        H[i, indices[i]:indices[i+1]] = 1
    return H

def generate_random_demodulator(W, R, seed=0):
    np.random.seed(seed)
    F = np.fft.fft(np.eye(W)) / np.sqrt(W)
    signs = np.random.choice([1, -1], size=W)
    D = np.diag(signs)
    H = build_accumulator_matrix(W, R)
    Phi = np.real(H @ D @ F)
    return Phi, F, D, H
