# Mínimos cuadrados reponderados iterativamente (IRLS) :black_square_button:

El algoritmo IRLS busca **reconstruir una señal escasa (sparse)** a partir de mediciones incompletas o indirectas, muy útil cuando una señal recibida tiene ruido o datos faltantes, como puede ser en la transmición de datos de forma serial.

## ¿Qué problema resuelve el algoritmo IRLS?

El objetivo es recuperar un vector escaso \( x \in \mathbb{R}^n \) a partir de mediciones comprimidas \( y \in \mathbb{R}^m \), donde \( m < n \). Esto se formula como un problema de minimización convexa:

\[
\min_{x} \| x \|_1 \quad \text{sujeto a} \quad A x = y
\]

### Definiciones

- **Matriz de medición** \( A \in \mathbb{R}^{m \times n} \):  
  Matriz no cuadrada (submuestreada) que codifica las restricciones lineales.
- **Vector desconocido** \( x \in \mathbb{R}^n \):  
  Señal original que se desea reconstruir (con mayoría de componentes cercanos a cero).
- **Medición observada** \( y \in \mathbb{R}^m \):  
  Datos recibidos (ej.: tramas Modbus desde Arduino).

### Norma L1

La norma \( \ell_1 \) promueve escasez en la solución:
\[
\| x \|_1 = \sum_{i=1}^n |x_i|
\]

## Aplicación en LabVIEW

1. **Adquisición de Datos**:  
   Leer \( y \) desde Arduino vía protocolo Modbus (usando nodos VISA en LabVIEW).  
2. **Resolución del Problema**:  
   Implementar el algoritmo IRLS (Iteratively Reweighted Least Squares) para resolver:
   \[
   x^* = \argmin_{x} \| x \|_1 \quad \text{s.t.} \quad A x = y
   \]
3. **Visualización**:  
   Graficar \( x^* \) reconstruido en un `Waveform Graph`.

## Ejemplo de Código (Pseudocódigo)

```python
# Ejemplo en Python para integración con LabVIEW
import numpy as np
from scipy.optimize import linprog

# Datos desde Modbus (y) y matriz A predefinida
y = np.array([...])  # Mediciones
A = np.array([...])  # Matriz de sensado

# Resolver minimización L1 (usando aproximación LP)
c = np.ones(2 * n)  # Variables: [x⁺, x⁻]
A_eq = np.hstack([A, -A])  # Restricción: A(x⁺ - x⁻) = y
bounds = [(0, None)] * (2 * n)
result = linprog(c, A_eq=A_eq, b_eq=y, bounds=bounds)
x_reconstruido = result.x[:n] - result.x[n:]
```

## Notas

- La matriz \( A \) debe satisfacer propiedades como **RIP** (Restricted Isometry Property) para garantizar reconstrucción exacta.  
- Para señales no escasas en el dominio original, aplicar transformadas (ej.: FFT) antes de la optimización.
