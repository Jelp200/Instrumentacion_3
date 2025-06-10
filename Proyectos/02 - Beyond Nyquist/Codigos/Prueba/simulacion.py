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

#* Generar matriz de medición Φ = H D F
Phi, F, D, H = generate_random_demodulator(W=W, R=R, seed=123)

#* Obteneción de mediciones comprimidas
y = Phi @ s_true

#* Recuperación de la señal usando IRLS
s_rec = np.array(irls(Phi, y))

#! Errores
error_l2 = np.linalg.norm(s_true - s_rec, 2)
print(f"Error de reconstrucción L2: {error_l2:.4f}")

#* Tiempo reconstruido
x_rec_time = np.real(np.fft.ifft(s_rec * np.sqrt(W)))
x_true_time = np.real(np.fft.ifft(s_true * np.sqrt(W)))

#* Gráfica combinada: espectro y tiempo
fig, axes = plt.subplots(2, 1, figsize=(10, 8))  # Dos filas, una columna

# Gráfica del espectro (magnitud de s)
axes[0].plot(np.abs(s_true), label='Original (|s|)')
axes[0].plot(np.abs(s_rec), '--', label='Recuperado (|s|)')
axes[0].set_title("Recuperación de señal escasa en frecuencia (|s|)")
axes[0].set_xlabel("Frecuencia")
axes[0].set_ylabel("Magnitud")
axes[0].legend()
axes[0].grid(True)

# Gráfica en el dominio del tiempocls
axes[1].plot(x_true_time, label='Original (tiempo)')
axes[1].plot(x_rec_time, '--', label='Recuperado (tiempo)')
axes[1].set_title("Reconstrucción en el dominio del tiempo")
axes[1].set_xlabel("Muestra")
axes[1].set_ylabel("Amplitud")
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.show()