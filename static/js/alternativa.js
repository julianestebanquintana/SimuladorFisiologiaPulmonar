document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('simulador-form');

  let chartVolumen, chartPresion, chartFlujo;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    // Obtener valores del formulario
    const compliance = parseFloat(document.getElementById('compliance').value) / 1000;
    const resistencia = parseFloat(document.getElementById('resistencia').value);
    const frecuencia = parseFloat(document.getElementById('frecuencia').value);
    const vt = parseFloat(document.getElementById('vt').value) / 1000;
    const duracion = parseFloat(document.getElementById('duracion').value);

    const url = `/simular?compliance=${compliance}&resistencia=${resistencia}&frecuencia=${frecuencia}&vt=${vt}&duracion=${duracion}`;

    try {
      const response = await fetch(url);
      const data = await response.json();

      const labels = data.time;

      // Destruir gráficos anteriores si existen
      if (chartVolumen) chartVolumen.destroy();
      if (chartPresion) chartPresion.destroy();
      if (chartFlujo) chartFlujo.destroy();

      // Crear gráfico de Volumen
      const ctxVolumen = document.getElementById('grafica-volumen').getContext('2d');
      chartVolumen = new Chart(ctxVolumen, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Volumen (L)',
            data: data.volume,
            borderColor: 'blue',
            tension: 0.3,
            fill: false
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Curva de Volumen'
            }
          },
          scales: {
            x: {
              title: { display: true, text: 'Tiempo (s)' }
            },
            y: {
              title: { display: true, text: 'Volumen (L)' }
            }
          }
        }
      });

      // Crear gráfico de Presión
      const ctxPresion = document.getElementById('grafica-presion').getContext('2d');
      chartPresion = new Chart(ctxPresion, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Presión (cmH₂O)',
            data: data.pressure,
            borderColor: 'red',
            tension: 0.3,
            fill: false
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Curva de Presión'
            }
          },
          scales: {
            x: {
              title: { display: true, text: 'Tiempo (s)' }
            },
            y: {
              title: { display: true, text: 'Presión (cmH₂O)' }
            }
          }
        }
      });

      // Crear gráfico de Flujo
      const ctxFlujo = document.getElementById('grafica-flujo').getContext('2d');
      chartFlujo = new Chart(ctxFlujo, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Flujo (L/s)',
            data: data.flow,
            borderColor: 'green',
            tension: 0.3,
            fill: false
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Curva de Flujo'
            }
          },
          scales: {
            x: {
              title: { display: true, text: 'Tiempo (s)' }
            },
            y: {
              title: { display: true, text: 'Flujo (L/s)' }
            }
          }
        }
      });

    } catch (error) {
      console.error('Error en la simulación (Vista 2):', error);
      alert('Ocurrió un error al obtener la simulación (Vista 2).');
    }
  });

  // Ejecutar simulación inicial
  form.dispatchEvent(new Event('submit'));
});
