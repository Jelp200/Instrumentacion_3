import numpy as np
import matplotlib.pyplot as plt
from random_demodulator import generate_random_demodulator
from irls import irls

#* PARAMETROS DEL SISTEMA
W = 128  # Tamaño de la señal original (f)
R = 32   # Número de muestras (Compresión)

#* Creación de la señal escasa en 'f' (Solo algunas componentes activas)
s_true = np.zeros(W)
s_true[[5, 20, 50]] = [1.5, -2.0, 1.0]  # frecuencias activas

#* Generar matriz de medición Φ como H D F
Phi, F, D, H = generate_random_demodulator(W=W, R=R, seed=123)

#* Obteneción de mediciones comprimidas
y = Phi @ s_true

#* Recuperación de la señal usando IRLS
s_rec = irls(Phi, y)

#* Mostrar resultados
plt.figure(figsize=(10, 4))
plt.plot(np.abs(s_true), label='Original (|s|)')
plt.plot(np.abs(s_rec), '--', label='Recuperado (|s|)')
plt.title("Recuperación de señal escasa en frecuencia (Beyond Nyquist)")
plt.xlabel("Índice de frecuencia")
plt.ylabel("Magnitud")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
