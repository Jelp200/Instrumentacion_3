import numpy as np

def build_accumulator_matrix(W, R):
    """
    Construcción de la matriz H que acumula W elementos en R bloques
    """
    block_size = W // R
    H = np.zeros((R, W))
    for i in range(R):
        H[i, i * block_size : (i + 1) * block_size] = 1
    return H

def generate_random_demodulator(W, R, seed=0):
    """
    Generar la matriz Φ = H D F como en el modelo Random Demodulator
    """
    np.random.seed(seed)
    F = np.fft.fft(np.eye(W)) / np.sqrt(W)  # matriz de Fourier
    signs = np.random.choice([1, 0], size=W)
    D = np.diag(signs)
    H = build_accumulator_matrix(W, R)
    Phi = np.real(H @ D @ F)  # Usamos la parte real
    return Phi, F, D, H
