# IRLS for Sparse Signal Recovery

This method solves:

    min ||x||_1 subject to Ax = y

It promotes sparsity in `x` and is suitable when signals are undersampled, as in compressed sensing.

In this system, Arduino performs pseudo-random modulation and LabVIEW uses IRLS to reconstruct the original signal.
