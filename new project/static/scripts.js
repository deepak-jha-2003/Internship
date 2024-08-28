document.querySelectorAll('.device-form').forEach(form => {
    const device = form.getAttribute('data-device');
    const select = form.querySelector('select');

    select.addEventListener('change', function () {
        const status = this.value;

        fetch('/toggle_device', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ device: device, status: status })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('energy').textContent = data.total_energy;
        })
        .catch(error => console.error('Error:', error));
    });
});
