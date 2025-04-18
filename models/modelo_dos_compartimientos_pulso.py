
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parámetros del modelo
R1 = 10              # Resistencia compartimiento 1
C1 = 1 / 500         # Compliance compartimiento 1
R2 = 25              # Resistencia compartimiento 2
C2 = 1 / 1500        # Compliance compartimiento 2
P0 = 500             # Presión del pulso
b = 0.25             # Duración del pulso (s)
t_final = 2          # Tiempo total de simulación
V1_0 = 0             # Volumen inicial compartimiento 1
V2_0 = 0             # Volumen inicial compartimiento 2

# Función de presión tipo pulso
def presion_pulso(t):
    return P0 if 0 <= t < b else 0

# Sistema de ecuaciones diferenciales
def modelo_dos_pulso(t, V):
    V1, V2 = V
    P = presion_pulso(t)
    dV1dt = (P - V1 / C1) / R1
    dV2dt = (P - V2 / C2) / R2
    return [dV1dt, dV2dt]

# Tiempo de simulación
t_eval = np.linspace(0, t_final, 500)

# Resolver sistema
sol = solve_ivp(modelo_dos_pulso, [0, t_final], [V1_0, V2_0], t_eval=t_eval)

# Calcular volumen total
V_total = sol.y[0] + sol.y[1]

# Graficar
plt.figure(figsize=(8, 5))
plt.plot(sol.t, sol.y[0], label='V1 (R1=10, C1=1/500)')
plt.plot(sol.t, sol.y[1], label='V2 (R2=25, C2=1/1500)')
plt.plot(sol.t, V_total, label='V total', linewidth=2.5, linestyle='--')
plt.axvline(b, color='r', linestyle='--', alpha=0.5, label=f'Fin del pulso (t = {b}s)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Volumen (mL o unidades arbitrarias)')
plt.title('Modelo de dos compartimientos (entrada tipo pulso)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
