
document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('grafica').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Volumen pulmonar (mL)',
                data: [],
                fill: false,
                borderColor: 'rgb(0, 123, 255)',
                tension: 0.2
            }]
        },
        options: {
            animation: false,
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Tiempo (s)' } },
                y: { title: { display: true, text: 'Volumen (mL)' } }
            }
        }
    });

    let intervalo;

    document.getElementById('simulador-form').addEventListener('submit', function (event) {
        event.preventDefault();
        clearInterval(intervalo);
        chart.data.labels = [];
        chart.data.datasets[0].data = [];
        chart.update();

        const parametros = {
            compliance: parseFloat(document.getElementById('compliance').value),
            resistencia: parseFloat(document.getElementById('resistencia').value),
            frecuencia: parseFloat(document.getElementById('frecuencia').value),
            fio2: parseFloat(document.getElementById('fio2').value),
            peep: parseFloat(document.getElementById('peep').value),
            vt: parseFloat(document.getElementById('vt').value)
        };

        let tiempo = 0;
        const dt = 0.1;
        intervalo = setInterval(() => {
            fetch('/simular', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ...parametros, tiempo })
            })
            .then(res => res.json())
            .then(data => {
                chart.data.labels.push(data.tiempo.toFixed(1));
                chart.data.datasets[0].data.push(data.volumen);
                chart.update();
                tiempo += dt;
                if (chart.data.labels.length > 100) {
                    chart.data.labels.shift();
                    chart.data.datasets[0].data.shift();
                }
            });
        }, dt * 1000);
    });
});
