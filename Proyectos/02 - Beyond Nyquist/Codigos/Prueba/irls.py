import numpy as np

def generate_modulation_matrix(n, m, pseudo_seq=None, sample_indices=None, seed=None):
    if seed is not None:
        np.random.seed(seed)

    if pseudo_seq is None:
        pseudo_seq = np.random.choice([1, -1], size=n)

    mod_matrix = np.diag(pseudo_seq)

    if sample_indices is None:
        sample_indices = np.sort(np.random.choice(np.arange(n), size=m, replace=False))

    #* MATRIZ FINAL m x n
    A = mod_matrix[sample_indices, :]

    return A, pseudo_seq, sample_indices

def irls(A, y, max_iter=50, tol=1e-5, epsilon=1e-8):
    m, n = A.shape
    #* Inicialización con ceros
    x = np.zeros(n)

    for i in range(max_iter):
        W = np.diag(1 / (np.abs(x) + epsilon))
        Aw = A @ W
        x_new = W @ np.linalg.lstsq(Aw, y, rcond=None)[0]
        if np.linalg.norm(x - x_new, 1) < tol:
            break
        x = x_new

    return x.tolist()
