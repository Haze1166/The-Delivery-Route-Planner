document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('planner-form');
    const loader = document.getElementById('loader');
    const resultsArea = document.getElementById('results-area');
    const errorContainer = document.getElementById('error-container');
    let map = null;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        resultsArea.classList.remove('visible');
        errorContainer.classList.add('hidden');
        loader.classList.remove('hidden');

        try {
            const response = await fetch('/api/plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ capacity: document.getElementById('capacity').value }),
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error);
            displayResults(data);
        } catch (error) {
            errorContainer.textContent = `Error: ${error.message}`;
            errorContainer.classList.remove('hidden');
        } finally {
            loader.classList.add('hidden');
        }
    });

    function displayResults(data) {
        document.getElementById('total-weight').textContent = `Total Weight: ${data.total_weight}kg`;
        document.getElementById('total-priority').textContent = `Total Priority: ${data.total_priority}`;
        const manifestBody = document.getElementById('manifest-table-body');
        manifestBody.innerHTML = '';
        data.manifest.forEach(pkg => {
            const row = document.createElement('tr');
            row.innerHTML = `<td>${pkg.package_id}</td><td>${pkg.destination}</td><td>${pkg.weight_kg}</td><td>${pkg.priority}</td>`;
            manifestBody.appendChild(row);
        });

        const routePath = document.getElementById('route-path');
        if (data.route_names && data.route_names.length > 0) {
            routePath.innerHTML = data.route_names.join(' &rarr; ');
            initializeMap(data);
        } else {
            routePath.textContent = 'Route could not be calculated.';
            document.getElementById('map').innerHTML = '';
        }
        resultsArea.classList.add('visible');
    }

    function initializeMap(data) {
        if (map) map.remove();
        if (!data.route_coords || data.route_coords.length === 0) return;
        
        map = L.map('map').setView(data.route_coords[0], 5);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        const warehouseIcon = L.icon({ iconUrl: '/static/img/depot.png', iconSize: [40, 40], iconAnchor: [20, 40] });
        const packageIcon = L.icon({ iconUrl: '/static/img/package.png', iconSize: [32, 32], iconAnchor: [16, 32] });
        
        data.route_names.forEach((name, i) => {
            L.marker(data.route_coords[i], { icon: name === 'Warehouse' ? warehouseIcon : packageIcon })
                .addTo(map).bindPopup(`<b>${name}</b>`);
        });

        const polyline = L.polyline(data.route_coords, { color: '#007bff' }).addTo(map);
        map.fitBounds(polyline.getBounds().pad(0.1));
    }
});