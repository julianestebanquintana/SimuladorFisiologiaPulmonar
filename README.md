# Simulador de Fisiología Pulmonar

Este proyecto es un simulador interactivo para el aprendizaje de fisiología pulmonar, orientado a estudiantes de medicina y profesionales de ciencias de la salud. Permite visualizar dinámicamente curvas de volumen pulmonar en respuesta a parámetros clínicos ajustables.

## 🚀 Características principales

- Interfaz web responsiva y amigable
- Parámetros clínicos ajustables:
  - Compliance pulmonar
  - Resistencia de la vía aérea
  - Frecuencia respiratoria
  - Fracción inspirada de oxígeno (FiO₂)
  - PEEP
  - Volumen corriente (VT)
- Gráfica en tiempo real de volumen pulmonar
- Backend en Flask
- Basado en un modelo fisiológico simplificado del sistema respiratorio

## 📦 Instalación

1. Clona este repositorio:

```bash
git clone <URL-del-repo>
cd SimuladorFisiologiaPulmonar
```

2. Instala dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecuta el servidor:

```bash
python app.py
```

4. Abre tu navegador en:

```
http://localhost:5000
```

## 📁 Estructura del proyecto

```
SimuladorFisiologiaPulmonar/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── js/
│   │   └── script.js
│   └── css/
│       └── style.css
```

## 📝 Licencia

Proyecto académico sin fines comerciales. Uso libre con atribución.

---
Versión: v0.1.0-mvp