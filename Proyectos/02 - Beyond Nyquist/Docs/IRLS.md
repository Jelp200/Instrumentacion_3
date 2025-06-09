# Mínimos cuadrados reponderados iterativamente (IRLS) :black_square_button:

El algoritmo IRLS busca **reconstruir una señal escasa (sparse)** a partir de mediciones incompletas o indirectas, muy útil cuando una señal recibida tiene ruido o datos faltantes, como puede ser en la transmición de datos de forma serial.

## ¿Qué problema resuelve el algoritmo IRLS?

Busca resolver el siguiente problema de minimización convexa:

![equation](https://latex.codecogs.com/svg.image?\min_{x}%20\|%20x%20\|_1%20\quad%20\text{sujeto%20a}%20\quad%20Ax%20=%20y)

Con el objetivo es recuperar un vector escaso: ![equation](https://latex.codecogs.com/svg.image?x%20\in%20\mathbb{R}^n), a partir de mediciones comprimidas: ![equation](https://latex.codecogs.com/svg.image?y%20\in%20\mathbb{R}^m) donde "![equation](https://latex.codecogs.com/svg.image?m%20<%20n)".  

### Definiciones

- **Matriz de medición ![equation](https://latex.codecogs.com/svg.image?A%20\in%20\mathbb{R}^{m%20\times%20n})**: Matriz no cuadrada (submuestreada) que codifica las restricciones lineales.
- **Vector desconocido**  
  ![equation](https://latex.codecogs.com/svg.image?x%20\in%20\mathbb{R}^n):  
  Señal original que se desea reconstruir (con mayoría de componentes cercanos a cero).
- **Medición observada**  
  ![equation](https://latex.codecogs.com/svg.image?y%20\in%20\mathbb{R}^m):  
  Datos recibidos (ej.: tramas Modbus desde Arduino).

### Norma L1

La norma L1 promueve escasez en la solución:

![equation](https://latex.codecogs.com/svg.image?\|%20x%20\|_1%20=%20\sum_{i=1}^n%20|x_i|)

## Aplicación en LabVIEW

1. **Adquisición de Datos**:  
   Leer ![equation](https://latex.codecogs.com/svg.image?y) desde Arduino vía protocolo Modbus (usando nodos VISA en LabVIEW).  
2. **Resolución del Problema**:  
   Implementar el algoritmo IRLS (Iteratively Reweighted Least Squares) para resolver:

   ![equation](https://latex.codecogs.com/svg.image?x^*%20=%20\arg\min_{x}%20\|%20x%20\|_1%20\quad%20\text{s.t.}%20\quad%20Ax%20=%20y)

3. **Visualización**:  
   Graficar ![equation](https://latex.codecogs.com/svg.image?x^*) reconstruido en un `Waveform Graph`.

## Ejemplo de Código (Pseudocódigo)

```python
# Ejemplo en Python para integración con LabVIEW
import numpy as np
from scipy.optimize import linprog

# Datos desde Modbus (y) y matriz A predefinida
y = np.array([...])  # Mediciones
A = np.array([...])  # Matriz de sensado
n = A.shape[1]

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
