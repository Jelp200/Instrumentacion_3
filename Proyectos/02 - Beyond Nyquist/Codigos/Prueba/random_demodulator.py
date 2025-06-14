import numpy as np

#* CONSTRUCCIÓN DE LA MATRIZ 'H' QUE ACUMULA 'W' ELEMENTOS EN R BLOQUES
def build_accumulator_matrix(W, R):
    if R > W:
        raise ValueError("R no debe ser mayor que W.")
    H = np.zeros((R, W))
    indices = np.linspace(0, W, R + 1, dtype=int)
    for i in range(R):
        H[i, indices[i]:indices[i+1]] = 1
    return H

#* generar la matriz 'Φ = H D F' COMO EL MODELO
def generate_random_demodulator(W, R, seed=0):
    np.random.seed(seed)
    F = np.fft.fft(np.eye(W)) / np.sqrt(W)  # matriz de Fourier
    signs = np.random.choice([1, 0], size=W)
    D = np.diag(signs)
    H = build_accumulator_matrix(W, R)
    Phi = np.real(H @ D @ F)  # Usamos la parte real
    return Phi, F, D, H
