import numpy as np
import matplotlib.pyplot as plt
from random_demodulator import generate_random_demodulator
from irls import irls

# Entrada del usuario
try:
    W = int(input("Ingrese la longitud de la señal original (W): "))
    R = int(input("Ingrese el número de muestras comprimidas (R): "))

    if R > W:
        raise ValueError("R no debe ser mayor que W.")

    # Señal escasa en frecuencia
    s_true = np.zeros(W)
    np.random.seed(42)
    indices = np.random.choice(W, 5, replace=False)
    s_true[indices] = np.random.uniform(-2, 2, size=5)

    #* Construcción de Φ = H D F
    Phi, F, D, H = generate_random_demodulator(W=W, R=R, seed=123)

    # Mediciones comprimidas
    y = Phi @ s_true

    # Recuperación
    s_rec = np.array(irls(Phi, y))

    # Errores
    error_l2 = np.linalg.norm(s_true - s_rec, 2)
    print(f"Error de reconstrucción L2: {error_l2:.4f}")

    # Tiempo reconstruido
    x_rec_time = np.real(np.fft.ifft(s_rec * np.sqrt(W)))
    x_true_time = np.real(np.fft.ifft(s_true * np.sqrt(W)))

    # Gráfica espectro
    plt.figure(figsize=(10, 4))
    plt.plot(np.abs(s_true), label='Original (|s|)')
    plt.plot(np.abs(s_rec), '--', label='Recuperado (|s|)')
    plt.title("Recuperación de señal escasa en frecuencia (|s|)")
    plt.xlabel("Frecuencia")
    plt.ylabel("Magnitud")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Gráfica en el dominio del tiempo
    plt.figure(figsize=(10, 4))
    plt.plot(x_true_time, label='Original (tiempo)')
    plt.plot(x_rec_time, '--', label='Recuperado (tiempo)')
    plt.title("Reconstrucción en el dominio del tiempo")
    plt.xlabel("Muestra")
    plt.ylabel("Amplitud")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

except ValueError as e:
    print(f"Error: {e}")
