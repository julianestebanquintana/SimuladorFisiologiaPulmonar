
from flask import Flask, render_template, request, send_file
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simular', methods=['POST'])
def simular():
    data = request.get_json()
    modelo = data['modelo']
    entrada = data['entrada']
    R = float(data['R'])
    C = float(data['C'])
    amp = float(data['amp'])
    dur_freq = float(data['dur_freq'])  # será usado como frecuencia si entrada == seno

    t_final = 2
    V0 = 0
    t_eval = np.linspace(0, t_final, 500)

    # Entradas
    def escalon(t): return amp
    def pulso(t): return amp if 0 <= t < dur_freq else 0
    def seno(t): return amp * np.sin(2 * np.pi * dur_freq * t)

    if entrada == 'escalon':
        P = escalon
    elif entrada == 'pulso':
        P = pulso
    elif entrada == 'seno':
        if dur_freq < 0.5:
            dur_freq = 3  # corrección automática si es demasiado baja
        P = seno
    else:
        return "Tipo de entrada no válido", 400

    if modelo == '1c':
        def modelo1(t, V):
            return (P(t) - V / C) / R
        sol = solve_ivp(modelo1, [0, t_final], [V0], t_eval=t_eval)
        volumen = sol.y[0]
        labels = ['Volumen']
    elif modelo == '2c':
        R1, C1 = R, C
        R2, C2 = R * 1.5, C / 3

        def modelo2(t, V):
            V1, V2 = V
            p = P(t)
            dV1dt = (p - V1 / C1) / R1
            dV2dt = (p - V2 / C2) / R2
            return [dV1dt, dV2dt]

        sol = solve_ivp(modelo2, [0, t_final], [0, 0], t_eval=t_eval)
        V1, V2 = sol.y
        volumen = [V1, V2, V1 + V2]
        labels = ['V1', 'V2', 'V total']
    else:
        return "Modelo no válido", 400

    # Graficar
    fig, ax = plt.subplots()
    if modelo == '1c':
        ax.plot(sol.t, volumen, label=labels[0])
    else:
        for v, label in zip(volumen, labels):
            ax.plot(sol.t, v, label=label)
    ax.set_title(f"Modelo {modelo} - Entrada {entrada}")
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Volumen (unidades arbitrarias)")
    ax.grid(True)
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
