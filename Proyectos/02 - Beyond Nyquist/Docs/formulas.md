# Key Formulas: IRLS

## Problem

    min_x ||x||_1 subject to Ax = y

## IRLS Approximation

    w_j = 1 / (|x_j| + epsilon)

    x^(n+1) = argmin_x ||W^(n) A x - W^(n) y||_2^2
