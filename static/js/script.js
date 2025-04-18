document.addEventListener('DOMContentLoaded', function () {
    const entrada = document.getElementById('entrada');
    const durFreqInput = document.getElementById('dur_freq');
    const durFreqLabel = durFreqInput.closest('.col-md-3').querySelector('label');

    function actualizarEtiqueta() {
        if (entrada.value === 'pulso') {
            durFreqLabel.textContent = 'Duración del pulso (s)';
        } else if (entrada.value === 'seno') {
            durFreqLabel.textContent = 'Frecuencia (Hz)';
        } else {
            durFreqLabel.textContent = 'Duración / Frecuencia';
        }
    }

    entrada.addEventListener('change', actualizarEtiqueta);
    actualizarEtiqueta();

    document.getElementById('simulador-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const datos = {
            modelo: document.getElementById('modelo').value,
            entrada: document.getElementById('entrada').value,
            R: parseFloat(document.getElementById('R').value),
            C: parseFloat(document.getElementById('C').value),
            amp: parseFloat(document.getElementById('amp').value),
            dur_freq: parseFloat(document.getElementById('dur_freq').value)
        };

        fetch('/simular', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        })
        .then(res => res.blob())
        .then(blob => {
            document.getElementById('grafica').src = URL.createObjectURL(blob);
        });
    });
});
