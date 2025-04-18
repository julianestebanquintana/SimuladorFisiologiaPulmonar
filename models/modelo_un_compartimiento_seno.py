import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parámetros del modelo
R = 15             # Resistencia (cmH2O·s/L)
C = 1 / 800        # Compliance (L/cmH2O)
A = 150            # Amplitud de la presión senoidal (Pa)
f = 3              # Frecuencia (Hz)
t_final = 2        # Duración de la simulación
V0 = 0             # Volumen inicial

# Función de presión tipo seno
def presion_seno(t):
    return A * np.sin(2 * np.pi * f * t)

# Modelo: dV/dt = (P(t) - V/C) / R
def modelo_seno(t, V):
    P = presion_seno(t)
    dVdt = (P - V / C) / R
    return dVdt

# Tiempo de simulación
t_eval = np.linspace(0, t_final, 500)

# Resolver la ODE
sol = solve_ivp(modelo_seno, [0, t_final], [V0], t_eval=t_eval)

# Graficar resultado
plt.figure(figsize=(8, 5))
plt.plot(sol.t, sol.y[0], label='Volumen pulmonar $V(t)$')
plt.xlabel('Tiempo (s)')
plt.ylabel('Volumen (mL o unidades arbitrarias)')
plt.title('Respuesta del volumen a una presión senoidal')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
