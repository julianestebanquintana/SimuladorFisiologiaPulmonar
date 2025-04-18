
from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')  # <-- Forzar backend no interactivo
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
    dur_freq = float(data['dur_freq'])

    t_final = 2
    V0 = 0
    t_eval = np.linspace(0, t_final, 500)

    def escalon(t): return amp
    def pulso(t): return amp if 0 <= t < dur_freq else 0
    def seno(t): return amp * np.sin(2 * np.pi * dur_freq * t)

    if entrada == 'escalon':
        P = escalon
    elif entrada == 'pulso':
        P = pulso
    elif entrada == 'seno':
        P = seno
    else:
        return "Tipo de entrada no válido", 400

    if modelo == '1c':
        def modelo1(t, V):
            return (P(t) - V / C) / R
        sol = solve_ivp(modelo1, [0, t_final], [V0], t_eval=t_eval)
        volumen = sol.y[0]
    else:
        return "Modelo no soportado aún", 400

    # Graficar
    fig, ax = plt.subplots()
    ax.plot(sol.t, volumen)
    ax.set_title(f"Modelo {modelo} - Entrada {entrada}")
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Volumen (unidades arbitrarias)")
    ax.grid(True)

    # Convertir gráfica a imagen en memoria
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
