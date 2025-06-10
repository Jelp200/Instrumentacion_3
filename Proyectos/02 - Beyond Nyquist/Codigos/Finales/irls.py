import numpy as np

def irls(A, y, max_iter=50, tol=1e-5, epsilon=1e-8):
    m, n = A.shape
    x = np.zeros(n)

    for i in range(max_iter):
        W = np.diag(1 / (np.abs(x) + epsilon))
        Aw = A @ W
        x_new = W @ np.linalg.lstsq(Aw, y, rcond=None)[0]
        if np.linalg.norm(x - x_new, 1) < tol:
            break
        x = x_new

    return x.tolist()
