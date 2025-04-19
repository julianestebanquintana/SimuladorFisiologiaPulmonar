from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simular', methods=['POST'])
def simular():
    data = request.get_json()
    t = data['tiempo']
    C = data['compliance'] / 1000  # convertir mL/cmH2O a L/cmH2O
    R = data['resistencia']        # cmH2O·s/L
    f = data['frecuencia']         # respiraciones por minuto
    VT = data['vt'] / 1000         # convertir mL a L
    PEEP = data['peep']

    # Frecuencia en Hz
    f_hz = f / 60
    # Presión senoidal + PEEP (entrada interna del modelo)
    P = PEEP + (VT / C) * np.sin(2 * np.pi * f_hz * t)
    # Volumen = C * P(t)
    V = C * P

    return jsonify({'tiempo': t, 'volumen': round(V * 1000, 2)})  # en mL

if __name__ == '__main__':
    app.run(debug=True)
