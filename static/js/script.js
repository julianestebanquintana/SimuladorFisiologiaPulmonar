document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('simulador-form');
  const ctx = document.getElementById('grafica').getContext('2d');
  const botonCSV = document.getElementById('descargarCSV');
  let chart;
  let datosSimulados = null; // Guardamos los datos de simulación

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    // Obtener valores del formulario
    const compliance = parseFloat(document.getElementById('compliance').value) / 1000; // mL/cmH2O → L/cmH2O
    const resistencia = parseFloat(document.getElementById('resistencia').value);
    const frecuencia = parseFloat(document.getElementById('frecuencia').value);
    const vt = parseFloat(document.getElementById('vt').value) / 1000; // mL → L
    const duracion = parseFloat(document.getElementById('duracion').value);

    // Construir URL con parámetros
    const url = `/simular?compliance=${compliance}&resistencia=${resistencia}&frecuencia=${frecuencia}&vt=${vt}&duracion=${duracion}`;

    try {
      const response = await fetch(url);
      const data = await response.json();

      datosSimulados = data; // Guardamos los datos para descarga

      const labels = data.time;

      // Destruir el gráfico anterior si ya existe
      if (chart) chart.destroy();

      // Crear nuevo gráfico con múltiples curvas
      chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Volumen (L)',
              data: data.volume,
              borderColor: 'blue',
              yAxisID: 'y',
              tension: 0.3
            },
            {
              label: 'Presión (cmH₂O)',
              data: data.pressure,
              borderColor: 'red',
              yAxisID: 'y1',
              tension: 0.3
            },
            {
              label: 'Flujo (L/s)',
              data: data.flow,
              borderColor: 'green',
              yAxisID: 'y2',
              tension: 0.3
            }
          ]
        },
        options: {
          responsive: true,
          interaction: {
            mode: 'index',
            intersect: false
          },
          stacked: false,
          plugins: {
            title: {
              display: true,
              text: 'Simulación respiratoria: Volumen, Presión y Flujo'
            },
            legend: {
              position: 'bottom'
            }
          },
          scales: {
            y: {
              type: 'linear',
              position: 'left',
              title: {
                display: true,
                text: 'Volumen (L)'
              }
            },
            y1: {
              type: 'linear',
              position: 'right',
              title: {
                display: true,
                text: 'Presión (cmH₂O)'
              },
              grid: {
                drawOnChartArea: false
              }
            },
            y2: {
              type: 'linear',
              position: 'right',
              offset: true,
              title: {
                display: true,
                text: 'Flujo (L/s)'
              },
              grid: {
                drawOnChartArea: false
              }
            }
          }
        }
      });
    } catch (error) {
      console.error('Error en la simulación:', error);
      alert('Ocurrió un error al obtener la simulación.');
    }
  });

  // Botón para descargar CSV
  botonCSV.addEventListener('click', () => {
    if (!datosSimulados) {
      alert('Primero debes realizar una simulación.');
      return;
    }

    const { time, volume, pressure, flow } = datosSimulados;
    let csv = 'tiempo (s),volumen (L),presión (cmH2O),flujo (L/s)\n';

    for (let i = 0; i < time.length; i++) {
      csv += `${time[i]},${volume[i]},${pressure[i]},${flow[i]}\n`;
    }

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'simulacion_pulmonar.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  });

  // Lanzar una simulación inicial al cargar la página
  form.dispatchEvent(new Event('submit'));
});
