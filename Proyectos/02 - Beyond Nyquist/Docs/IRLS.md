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

## Arquitectura de adquisición

Del paper y el [diagrama general del sistema](../Diagramas/D.png), es posible observar que del lado del microcontrolador `uC` se tiene una demodulación aleatoria, la cual.

| **_Paso_** | **_Acción_**                                                                   |
|------------|--------------------------------------------------------------------------------|
| 1.         | Multiplica la señal con una **secuencia pseudoaleatoria** de 1, 0 (modulación) |
| 2.         | Integra la señal en bloques                                                    |
| 3          | Muestra con ADC                                                                |

Esto implica que la **matriz de medición** `A` debe reflejar esta secuencia de pasos:

$$ \mathbf{ \phi = HDF} $$

![Demodulación aleatoria](../Diagramas/D%20(1).png)

## Aplicación en LabVIEW

1. **Adquisición de Datos:** Leer ![equation](https://latex.codecogs.com/svg.image?y) desde Arduino vía protocolo Modbus (usando nodos VISA en LabVIEW).  
2. **Resolución del Problema:** Implementar el algoritmo IRLS (Iteratively Reweighted Least Squares) para resolver:

   ![equation](https://latex.codecogs.com/svg.image?x^*%20=%20\arg\min_{x}%20\|%20x%20\|_1%20\quad%20\text{s.t.}%20\quad%20Ax%20=%20y)

3. **Visualización:** Graficar ![equation](https://latex.codecogs.com/svg.image?x^*) reconstruido en un `Waveform Graph`.

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
