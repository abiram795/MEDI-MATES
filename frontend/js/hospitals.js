import { request } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
    searchHospitals();
});

window.searchHospitals = async function() {
    const name = document.getElementById('search-name').value;

    let url = '/hospitals/';
    if (name) url += `?search=${encodeURIComponent(name)}`;

    const listDiv = document.getElementById('hospitals-list');
    listDiv.innerHTML = '<p>Loading hospitals...</p>';

    try {
        const hospitals = await request(url);
        renderHospitals(hospitals);
    } catch (error) {
        listDiv.innerHTML = `<p class="error">Error loading hospitals: ${error.message}</p>`;
    }
}

window.findNearby = function() {
    if (!navigator.geolocation) {
        alert("Geolocation is not supported by your browser.");
        return;
    }

    const listDiv = document.getElementById('hospitals-list');
    listDiv.innerHTML = '<p>Finding nearby hospitals...</p>';

    navigator.geolocation.getCurrentPosition(async (position) => {
        const userLat = position.coords.latitude;
        const userLng = position.coords.longitude;

        try {
            const hospitals = await request('/hospitals/');

            // Basic distance calculation in frontend since postgrest doesn't easily support haversine natively without custom RPC
            const withDistance = hospitals.map(h => {
                let dist = Infinity;
                if (h.hospital_locations && h.hospital_locations.length > 0) {
                    const loc = h.hospital_locations[0];
                    dist = getDistanceFromLatLonInKm(userLat, userLng, loc.latitude, loc.longitude);
                }
                return { ...h, distance: dist };
            });

            // Sort by distance and filter out those without location
            const sorted = withDistance.filter(h => h.distance !== Infinity).sort((a, b) => a.distance - b.distance);

            renderHospitals(sorted, true);
        } catch (error) {
             listDiv.innerHTML = `<p class="error">Error loading hospitals: ${error.message}</p>`;
        }
    }, () => {
        alert("Location access was not granted. Search hospitals by name instead.");
        searchHospitals();
    });
}

function renderHospitals(hospitals, showDistance = false) {
    const listDiv = document.getElementById('hospitals-list');
    if (hospitals.length > 0) {
        listDiv.innerHTML = hospitals.map(h => `
            <div class="card">
                <h3>${h.hospital_name}</h3>
                <p><strong>Type:</strong> ${h.hospital_type || 'General'}</p>
                <p><strong>Address:</strong> ${h.address || 'N/A'}</p>
                <p><strong>Phone:</strong> ${h.phone || 'N/A'}</p>
                ${showDistance ? `<p style="color: var(--primary); font-weight: bold;">Distance: ${h.distance.toFixed(1)} km</p>` : ''}
            </div>
        `).join('');
    } else {
        listDiv.innerHTML = '<p>No hospitals found.</p>';
    }
}

function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
    var R = 6371; // Radius of the earth in km
    var dLat = deg2rad(lat2-lat1);
    var dLon = deg2rad(lon2-lon1);
    var a =
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
        Math.sin(dLon/2) * Math.sin(dLon/2)
        ;
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    var d = R * c; // Distance in km
    return d;
}

function deg2rad(deg) {
    return deg * (Math.PI/180);
}
