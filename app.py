from flask import Flask, jsonify, request, render_template
import numpy as np

app = Flask(__name__)

def calcular_flujo(volumen, tiempo):
    volumen = np.array(volumen)
    tiempo = np.array(tiempo)
    flujo = np.gradient(volumen, tiempo)
    return flujo.tolist()

def calcular_presion(volumen, flujo, compliance, resistencia):
    volumen = np.array(volumen)
    flujo = np.array(flujo)
    presion = volumen / compliance + resistencia * flujo
    return presion.tolist()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simular')
def simular():
    # Parámetros clínicos básicos
    compliance = float(request.args.get("compliance", 0.05))     # L/cmH2O
    resistencia = float(request.args.get("resistencia", 5.0))    # cmH2O·s/L
    frecuencia = float(request.args.get("frecuencia", 12))       # respiraciones/min
    duracion = float(request.args.get("duracion", 10))           # segundos
    vt = float(request.args.get("vt", 0.5))                      # volumen tidal (L)

    # Tiempo total y resolución
    puntos_por_segundo = 100
    t = np.linspace(0, duracion, int(duracion * puntos_por_segundo))

    # Parámetros del ciclo respiratorio
    ciclo_duracion = 60 / frecuencia  # duración de un ciclo (segundos)
    tiempo_insp = 0.4 * ciclo_duracion
    tiempo_exp = 0.6 * ciclo_duracion

    flujo = np.zeros_like(t)
    volumen = np.zeros_like(t)

    for i, tiempo_actual in enumerate(t):
        tiempo_en_ciclo = tiempo_actual % ciclo_duracion
        if tiempo_en_ciclo < tiempo_insp:
            flujo[i] = vt / tiempo_insp
        else:
            tiempo_exp_actual = tiempo_en_ciclo - tiempo_insp
            flujo[i] = -vt * 5 * np.exp(-5 * tiempo_exp_actual / tiempo_exp) / tiempo_exp

    # Integración del volumen con reinicio por ciclo
    vol_actual = 0
    for i in range(1, len(t)):
        dt = t[i] - t[i - 1]
        tiempo_en_ciclo = t[i] % ciclo_duracion
        tiempo_prev_en_ciclo = t[i - 1] % ciclo_duracion

        if tiempo_en_ciclo < tiempo_prev_en_ciclo:
            vol_actual = 0  # reiniciar al inicio de nuevo ciclo

        vol_actual += flujo[i] * dt
        volumen[i] = vol_actual

    # Cálculo de la presión
    presion = calcular_presion(volumen, flujo, compliance, resistencia)

    return jsonify({
        "time": t.tolist(),
        "volume": volumen.tolist(),
        "flow": flujo.tolist(),
        "pressure": presion
    })

if __name__ == '__main__':
    app.run(debug=True)
