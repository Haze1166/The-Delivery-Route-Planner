document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('planner-form');
    const loader = document.getElementById('loader');
    const resultsContainer = document.getElementById('results-container');
    const errorContainer = document.getElementById('error-container');

    let map = null; // To hold the map instance

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Form submitted. Starting planning process...');

        // Reset UI state
        resultsContainer.innerHTML = ''; // Clear old results completely
        resultsContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
        loader.classList.remove('hidden');

        const capacity = document.getElementById('capacity').value;

        try {
            console.log(`Fetching plan for capacity: ${capacity}`);
            const response = await fetch('/api/plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ capacity: capacity }),
            });
            
            const data = await response.json();
            console.log('Received response from server:', data);

            if (!response.ok) {
                // Handle errors returned from the API (e.g., validation errors)
                throw new Error(data.error || `HTTP error! Status: ${response.status}`);
            }

            displayResults(data);

        } catch (error) {
            console.error('An error occurred during the fetch operation:', error);
            displayError(error.message);
        } finally {
            loader.classList.add('hidden');
        }
    });

    function displayError(message) {
        errorContainer.textContent = `Error: ${message}`;
        errorContainer.classList.remove('hidden');
    }

    function displayResults(data) {
        console.log('Displaying results...');
        
        // Build the manifest card HTML
        const manifestHTML = `
            <div class="card" id="manifest-card">
                <h2>Optimal Loading Manifest</h2>
                <div class="stats">
                    <span>Total Weight: ${data.total_weight}kg</span>
                    <span>Total Priority: ${data.max_priority}</span>
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr><th>ID</th><th>Destination</th><th>Weight</th><th>Priority</th></tr>
                        </thead>
                        <tbody>
                            ${data.manifest.map(pkg => `
                                <tr>
                                    <td>${pkg.package_id}</td>
                                    <td>${pkg.destination}</td>
                                    <td>${pkg.weight_kg}</td>
                                    <td>${pkg.priority}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        `;

        // Build the route card HTML
        const routeHTML = `
            <div class="card" id="route-card">
                <h2>Optimal Delivery Route</h2>
                ${data.route_names && data.route_names.length > 0
                    ? `<p class="route-path">${data.route_names.join(' &rarr; ')}</p><div id="map"></div>`
                    : `<p>Could not compute a valid round-trip route.</p>`
                }
            </div>
        `;

        // Inject the new HTML into the results container
        resultsContainer.innerHTML = manifestHTML + routeHTML;
        resultsContainer.classList.remove('hidden');

        // Initialize the map only if the route was successfully calculated
        if (data.route_names && data.route_names.length > 0) {
            initializeMap(data);
        }
        console.log('Results displayed successfully.');
    }

    function initializeMap(data) {
        console.log('Initializing map...');
        if (map) {
            map.remove(); // Remove old map instance if it exists
        }
        
        map = L.map('map').setView(data.route_coords[0], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        // Define custom icons
        const warehouseIcon = L.icon({ iconUrl: '/static/img/depot.png', iconSize: [40, 40], iconAnchor: [20, 40] });
        const packageIcon = L.icon({ iconUrl: '/static/img/package.png', iconSize: [32, 32], iconAnchor: [16, 32] });

        // Add markers to the map
        data.route_names.forEach((name, index) => {
            L.marker(data.route_coords[index], { icon: name === 'Warehouse' ? warehouseIcon : packageIcon })
                .addTo(map)
                .bindPopup(`<b>${index === 0 ? '' : `${index}. `}${name}</b>`);
        });

        const polyline = L.polyline(data.route_coords, { color: 'var(--primary-color)' }).addTo(map);
        map.fitBounds(polyline.getBounds().pad(0.1));
        console.log('Map initialized.');
    }
});