# irls.py
import numpy as np

def generate_modulation_matrix(n, m, pseudo_seq=None, sample_indices=None, seed=None):
    """
    Genera una matriz de medición A que simula la modulación pseudoaleatoria + muestreo comprimido.

    Args:
        n (int): Tamaño total de la señal original (longitud de x)
        m (int): Número de mediciones (longitud de y)
        pseudo_seq (array, optional): Secuencia pseudoaleatoria de ±1. Si no se da, se genera.
        sample_indices (array, optional): Índices de muestreo (selección de filas). Si no se da, se generan.
        seed (int, optional): Semilla para reproducibilidad

    Returns:
        A (ndarray): Matriz de medición (m x n)
        pseudo_seq (ndarray): Secuencia utilizada (±1)
        sample_indices (ndarray): Índices de las filas seleccionadas
    """
    if seed is not None:
        np.random.seed(seed)

    if pseudo_seq is None:
        pseudo_seq = np.random.choice([1, -1], size=n)

    mod_matrix = np.diag(pseudo_seq)

    if sample_indices is None:
        sample_indices = np.sort(np.random.choice(np.arange(n), size=m, replace=False))

    A = mod_matrix[sample_indices, :]  # matriz final m x n

    return A, pseudo_seq, sample_indices


def irls(A, y, max_iter=50, tol=1e-5, epsilon=1e-8):
    """
    IRLS - Iteratively Reweighted Least Squares para recuperación escasa
    Resuelve: min ||x||_1 sujeto a Ax = y

    Args:
        A (ndarray): Matriz de medición (m x n)
        y (ndarray): Vector de observaciones (m,)
        max_iter (int): Máx. iteraciones
        tol (float): Tolerancia de convergencia
        epsilon (float): Constante para evitar divisiones por cero

    Returns:
        x (list): Señal reconstruida (lista de floats)
    """
    m, n = A.shape
    x = np.linalg.pinv(A) @ y  # estimación inicial

    for i in range(max_iter):
        W = np.diag(1 / (np.abs(x) + epsilon))
        Aw = A @ W
        x_new = W @ np.linalg.lstsq(Aw, y, rcond=None)[0]

        if np.linalg.norm(x - x_new, 1) < tol:
            break
        x = x_new

    return x.tolist()
