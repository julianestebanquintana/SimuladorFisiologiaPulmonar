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
    # Parámetros clínicos básicos (pueden ser ajustables desde frontend)
    compliance = float(request.args.get("compliance", 0.05))     # L/cmH2O
    resistencia = float(request.args.get("resistencia", 5.0))    # cmH2O·s/L
    frecuencia = float(request.args.get("frecuencia", 12))       # respiraciones/min
    duracion = float(request.args.get("duracion", 10))           # segundos
    amplitud = float(request.args.get("vt", 0.5))                # volumen tidal (L)

    # Tiempo y volumen simulado (onda sinusoidal respiratoria)
    t = np.linspace(0, duracion, int(duracion * 100))  # 100 puntos por segundo
    volumen = amplitud * (1 + np.sin(2 * np.pi * frecuencia / 60 * t)) / 2

    # Flujo y presión
    flujo = calcular_flujo(volumen, t)
    presion = calcular_presion(volumen, flujo, compliance, resistencia)

    # Envío de datos al frontend
    return jsonify({
        "time": t.tolist(),
        "volume": volumen.tolist(),
        "flow": flujo,
        "pressure": presion
    })

if __name__ == '__main__':
    app.run(debug=True)
