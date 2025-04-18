import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parámetros del modelo
R = 15             # Resistencia (cmH2O·s/L)
C = 1 / 800        # Compliance (L/cmH2O)
P0 = 500           # Presión constante (Pa)
t_final = 2        # Duración de la simulación en segundos
V0 = 0             # Volumen inicial

# Escalón de presión
def presion(t):
    return P0 if t >= 0 else 0

# Ecuación diferencial: dV/dt = (P(t) - V/C) / R
def modelo(t, V):
    P = presion(t)
    dVdt = (P - V / C) / R
    return dVdt

# Tiempo de simulación
t_eval = np.linspace(0, t_final, 500)

# Resolver ODE
sol = solve_ivp(modelo, [0, t_final], [V0], t_eval=t_eval)

# Graficar
plt.figure(figsize=(8, 5))
plt.plot(sol.t, sol.y[0], label='Volumen pulmonar $V(t)$')
plt.xlabel('Tiempo (s)')
plt.ylabel('Volumen (mL o unidades arbitrarias)')
plt.title('Respuesta del volumen a un escalón de presión')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
