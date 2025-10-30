document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('planner-form');
    const loader = document.getElementById('loader');
    const resultsContainer = document.getElementById('results-container');
    const errorContainer = document.getElementById('error-container');

    let map = null; // To hold the map instance

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Reset UI
        resultsContainer.classList.add('results-hidden');
        errorContainer.classList.add('error-hidden');
        loader.classList.remove('loader-hidden');

        const capacity = document.getElementById('capacity').value;

        try {
            const response = await fetch('/api/plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ capacity: capacity }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'An unknown error occurred.');
            }

            displayResults(data);

        } catch (error) {
            displayError(error.message);
        } finally {
            loader.classList.add('loader-hidden');
        }
    });

    function displayError(message) {
        errorContainer.textContent = `Error: ${message}`;
        errorContainer.classList.remove('error-hidden');
    }

    function displayResults(data) {
        // Populate Manifest Table
        const manifestBody = document.getElementById('manifest-table-body');
        manifestBody.innerHTML = ''; // Clear previous results
        data.manifest.forEach(pkg => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${pkg.package_id}</td>
                <td>${pkg.destination}</td>
                <td>${pkg.weight_kg}</td>
                <td>${pkg.priority}</td>
            `;
            manifestBody.appendChild(row);
        });

        document.getElementById('total-weight').textContent = `Total Weight: ${data.total_weight}kg`;
        document.getElementById('total-priority').textContent = `Total Priority: ${data.max_priority}`;
        
        // Populate Route Information
        const routePath = document.getElementById('route-path');
        if (data.route_names && data.route_names.length > 0) {
            routePath.innerHTML = data.route_names.join(' &rarr; ');
            initializeMap(data);
        } else {
            routePath.textContent = 'Could not compute a valid round-trip route.';
            document.getElementById('map').innerHTML = '<p style="text-align:center; padding: 20px;">Map not available.</p>';
        }

        resultsContainer.classList.remove('results-hidden');
    }

    function initializeMap(data) {
        // Destroy previous map instance if it exists
        if (map) {
            map.remove();
        }
        
        const mapContainer = document.getElementById('map');
        map = L.map(mapContainer).setView(data.route_coords[0], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        // Custom Icons
        const warehouseIcon = L.icon({
            iconUrl: '/static/img/depot.png',
            iconSize: [40, 40],
            iconAnchor: [20, 40],
        });
        const packageIcon = L.icon({
            iconUrl: '/static/img/package.png',
            iconSize: [32, 32],
            iconAnchor: [16, 32],
        });

        // Add markers
        data.route_names.forEach((name, index) => {
            const coord = data.route_coords[index];
            const icon = name === 'Warehouse' ? warehouseIcon : packageIcon;
            L.marker(coord, { icon: icon }).addTo(map)
                .bindPopup(`<b>${index === 0 ? '' : `${index}. `}${name}</b>`);
        });

        // Draw polyline for the route
        const polyline = L.polyline(data.route_coords, { color: 'var(--primary-color)' }).addTo(map);
        map.fitBounds(polyline.getBounds().pad(0.1));
    }
});