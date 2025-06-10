# Mínimos cuadrados reponderados iterativamente (IRLS) :black_square_button:

El algoritmo IRLS busca **reconstruir una señal escasa (sparse)** a partir de mediciones incompletas o indirectas, muy útil cuando una señal recibida tiene ruido o datos faltantes, como puede ser en la transmición de datos de forma serial.

## ¿Qué problema resuelve el algoritmo IRLS?

Busca resolver el siguiente problema de minimización convexa:

$$ \mathbf{\underset{x}{min} \left | x \right |_{1}}\hspace{0.2cm}sujeto\hspace{0.2cm}a\hspace{0.2cm} \mathbf{Ax=y} $$

Con el objetivo es recuperar un vector escaso:

$$\mathbf{x \in \mathbb{R}^{n}}$$

A partir de mediciones comprimidas:

$$\mathbf{y \in \mathbb{R}^{n}} \hspace{0.2cm}donde\hspace{0.2cm} \mathbf{m< n}$$

### Definiciones

- **Matriz de medición:** Matriz no cuadrada (submuestreada) que codifica las restricciones lineales.

$$\mathbf{A \in \mathbb{R}^{m \times n}}$$

- **Vector desconocido:** Señal original que se desea reconstruir (con mayoría de componentes cercanos a cero).

$$\mathbf{x \in \mathbb{R}^{n}}$$

- **Medición observada:** Datos recibidos (tramas Modbus desde Arduino).

$$\mathbf{y \in \mathbb{R}^{m}}$$

### Norma L1

La norma L1 promueve escasez en la solución, es decir, que muchos elementos de `x` sean **exactamente cero**. Esto es útil si se sabe que la señal es naturalmente escasa:

![Norma L1](https://latex.codecogs.com/svg.latex?\left%20\|%20x%20\right%20\|_{1}%20=%20\sum_{i=1}^{n}%20\left%20|%20x_{i}%20\right%20|)

## Relación de IRLS con Beyond Nyquist

El paper de [Beyond Nyquist](Papers/) considera señales de la forma:

$$ f(t) = \sum_{a} a_{w} e^{e-2 \pi \omega t} $$

- Donde la señal es **escasa en frecuencia** (pocos tonos activos).
- El sistema busca recuperar los coeficientes $$\mathbf{a_{\omega}}$$ a partir de mediciones mucho menores a la de Nyquist.

### Arquitectura de adquisición

Del paper y el [diagrama general del sistema](../Diagramas/D.png), es posible observar que del lado del microcontrolador `uC` se tiene una demodulación aleatoria, la cual.

| **_Paso_** | **_Acción_**                                                                   |
|------------|--------------------------------------------------------------------------------|
| 1.         | Multiplica la señal con una **señal pseudoaleatoria** de 1, 0 (modulación) |
| 2.         | Integra la señal en bloques                                                    |
| 3          | Muestra con ADC                                                                |

![Demodulación aleatoria](../Diagramas/D%20(1).png)

Esto implica que la **matriz de medición** `A` debe reflejar esta secuencia de pasos:

$$ \mathbf{ \phi = HDF} $$

- $$F$$: Matriz de Fourier (base de la señal escasa).
- $$\mathbf{D = \mathrm{diag}(\varepsilon_0, \dots, \varepsilon_{W-1})},\hspace{0.2cm}\text{con }\varepsilon_i \in \left [ +1,\ 0 \right ]$$
- $$H$$: Matriz de acumulación (suma de bloques)

### Matriz del la demodulación aleatoria (Paper Beyond Nyquist)

Dado que ya se conoce que  la **matriz de medición** debe reflejar la secuencia de pasos que se muestra en la figura anterior, y que:

$$ \mathbf{ \phi = HDF} $$

Entonces:

- $$\mathbf{F \in \mathbb{C^{W\times W}}}$$: Matriz de Fourier discreta.
- $$D$$: Matriz diagonal con 1,0 (señal pseudoaleatoria).
- $$\mathbf{H\in\mathbb{R^{R\times W}}}$$: Realiza sumas por bloques

## Aplicación en LabVIEW

1. **Adquisición de Datos:** Leer ![equation](https://latex.codecogs.com/svg.image?y) desde Arduino vía protocolo Modbus (usando nodos VISA en LabVIEW).  
2. **Resolución del Problema:** Implementar el algoritmo IRLS (Iteratively Reweighted Least Squares) para resolver:

   ![equation](https://latex.codecogs.com/svg.image?x^*%20=%20\arg\min_{x}%20\|%20x%20\|_1%20\quad%20\text{s.t.}%20\quad%20Ax%20=%20y)

3. **Visualización:** Graficar ![equation](https://latex.codecogs.com/svg.image?x^*) reconstruido en un `Waveform Graph`.

## Código IRLS

```python
import numpy as np

#* GENERA LA MATRIZ DE MODULACIÓN
def generate_modulation_matrix(n, m, pseudo_seq=None, sample_indices=None, seed=None):
    if seed is not None:
        np.random.seed(seed)

    if pseudo_seq is None:
        pseudo_seq = np.random.choice([1, -1], size=n)

    mod_matrix = np.diag(pseudo_seq)

    if sample_indices is None:
        sample_indices = np.sort(np.random.choice(np.arange(n), size=m, replace=False))

    A = mod_matrix[sample_indices, :]  # Matrz final m x n

    return A, pseudo_seq, sample_indices

#* ALGORTIMO IRLS
def irls(A, y, max_iter=50, tol=1e-5, epsilon=1e-8):
    m, n = A.shape
    x = np.zeros(n)                    # Inicialización con ceros

    for i in range(max_iter):
        W = np.diag(1 / (np.abs(x) + epsilon))
        Aw = A @ W
        x_new = W @ np.linalg.lstsq(Aw, y, rcond=None)[0]
        if np.linalg.norm(x - x_new, 1) < tol:
            break
        x = x_new

    return x.tolist()
```

## Código demodulación aleatoria

```python
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
    F = np.fft.fft(np.eye(W)) / np.sqrt(W)      # Matriz de Fourier
    signs = np.random.choice([1, 0], size=W)
    D = np.diag(signs)
    H = build_accumulator_matrix(W, R)
    Phi = np.real(H @ D @ F)                    # Parte real
    return Phi, F, D, H
```

## Notas

- La matriz \( A \) debe satisfacer propiedades como **RIP** (Restricted Isometry Property) para garantizar reconstrucción exacta.  
- Para señales no escasas en el dominio original, aplicar transformadas (ej.: FFT) antes de la optimización.

### [Apartado anterior](../Inicio.md)
