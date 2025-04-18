import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parámetros del modelo
R = 15             # Resistencia (cmH2O·s/L)
C = 1 / 800        # Compliance (L/cmH2O)
P0 = 500           # Amplitud del pulso (Pa)
b = 0.25           # Duración del pulso (s)
t_final = 2        # Tiempo total de simulación
V0 = 0             # Volumen inicial

# Función de presión tipo pulso
def presion_pulso(t):
    return P0 if 0 <= t < b else 0

# Modelo: dV/dt = (P(t) - V/C) / R
def modelo_pulso(t, V):
    P = presion_pulso(t)
    dVdt = (P - V / C) / R
    return dVdt

# Tiempo de simulación
t_eval = np.linspace(0, t_final, 500)

# Resolver la ODE
sol = solve_ivp(modelo_pulso, [0, t_final], [V0], t_eval=t_eval)

# Graficar resultado
plt.figure(figsize=(8, 5))
plt.plot(sol.t, sol.y[0], label='Volumen pulmonar $V(t)$')
plt.axvline(b, color='r', linestyle='--', alpha=0.5, label=f'Fin del pulso (t = {b}s)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Volumen (mL o unidades arbitrarias)')
plt.title('Respuesta del volumen a un pulso de presión')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
